import csv
import io
import hmac
import hashlib
import base64
import uuid
from io import BytesIO
from decimal import Decimal, ROUND_HALF_UP
from django.conf import settings
from django.utils import timezone
from django.db.models import Avg
from apps.courses.models import CourseSection, InstitutionSetting
from apps.courses.services import get_institution_settings, convert_score_to_performance_level
from apps.subjects.models import Subject, KnowledgeArea
from apps.periods.models import AcademicPeriod
from apps.students.models import StudentProfile, Enrollment
from apps.teachers.models import TeachingAssignment
from apps.grades.models import EvaluationCriterion, GradeRecord, PeriodFinalGrade
from apps.attendance.models import AttendanceRecord

def generate_bulletin_crypto_token(student_id, period_id, average_score, year):
    """
    Genera un hash criptográfico HMAC-SHA256 inmutable para garantizar
    la autenticidad de las notas y evitar adulteraciones en impresiones o PDFs.
    """
    secret = getattr(settings, 'SECRET_KEY', 'academix-critical-key-2026')
    payload = f"ACADEMIX-BULLETIN|STUDENT:{student_id}|PERIOD:{period_id}|AVG:{average_score}|YEAR:{year}"
    token = hmac.new(secret.encode('utf-8'), payload.encode('utf-8'), hashlib.sha256).hexdigest()
    return token[:20].upper()

def generate_bulletin_qr_base64(verification_url):
    """
    Genera un código QR enlazado a la URL pública de verificación y lo devuelve en formato base64
    para incrustación directa en el PDF/HTML (data:image/png;base64,...).
    """
    try:
        import qrcode
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=4,
            border=2,
        )
        qr.add_data(verification_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#0f172a", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        encoded = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{encoded}"
    except Exception:
        return ""

def compile_weasyprint_pdf(html_string, base_url=None):
    """
    Compila el documento HTML optimizado con CSS Paged Media a PDF binario mediante WeasyPrint.
    Si el host del sistema carece de librerías nativas Pango/Cairo (común en Windows local sin GTK),
    captura el error y retorna (None, error_str) para permitir fallback seguro.
    """
    try:
        import weasyprint
        html_doc = weasyprint.HTML(string=html_string, base_url=base_url)
        pdf_bytes = html_doc.write_pdf()
        return pdf_bytes, None
    except Exception as e:
        return None, str(e)

def build_student_bulletin_data(student, section, period, request=None):
    """
    Construye la estructura completa de datos del Boletín Oficial de Calificaciones
    de un estudiante conforme al Decreto 1290 y las áreas del plan de estudios.
    Integra parametrización híbrida (Público/Privado), ranking, desempeños y firma criptográfica.
    """
    institution = get_institution_settings()
    academic_year = section.academic_year
    enrollment = Enrollment.objects.filter(
        student=student,
        course_section=section,
        academic_year=academic_year
    ).first()

    # Director de grupo o docente titular principal
    assignment_director = TeachingAssignment.objects.filter(
        course_section=section,
        academic_year=academic_year,
        is_active=True
    ).select_related('teacher__user').first()
    group_director = assignment_director.teacher if assignment_director else None

    # Áreas de conocimiento y asignaturas
    areas = KnowledgeArea.objects.all().order_by('name')
    bulletin_areas = []

    total_weighted_score = Decimal('0.00')
    total_subjects_count = 0
    total_failed_count = 0
    total_absences_period = 0

    for area in areas:
        area_subjects = Subject.objects.filter(area=area).order_by('name')
        subject_items = []
        area_score_sum = Decimal('0.00')
        area_sub_count = 0

        for sub in area_subjects:
            assignment = TeachingAssignment.objects.filter(
                course_section=section,
                subject=sub,
                academic_year=academic_year,
                is_active=True
            ).select_related('teacher__user').first()

            # Solo incluir asignaturas que tengan asignación o notas en esta sección
            final_grade = PeriodFinalGrade.objects.filter(
                student=student,
                course_section=section,
                subject=sub,
                academic_period=period
            ).first()

            if not assignment and not final_grade:
                continue

            # Criterios y notas
            criteria = EvaluationCriterion.objects.filter(
                course_section=section,
                subject=sub,
                academic_period=period
            ).order_by('order')

            criteria_details = []
            feedback_notes = []
            for crit in criteria:
                rec = GradeRecord.objects.filter(
                    student=student,
                    course_section=section,
                    subject=sub,
                    academic_period=period,
                    criterion=crit
                ).first()
                sc = rec.score if rec else Decimal('1.00')
                if rec and rec.feedback:
                    feedback_notes.append(rec.feedback)
                criteria_details.append({
                    'name': crit.name,
                    'percentage': crit.percentage,
                    'score': sc
                })

            # Faltas en el periodo
            absences = AttendanceRecord.objects.filter(
                student=student,
                session__course_section=section,
                session__subject=sub,
                session__academic_period=period
            )
            unjustified_abs = absences.filter(status=AttendanceRecord.Status.UNJUSTIFIED).count()
            justified_abs = absences.filter(status=AttendanceRecord.Status.JUSTIFIED).count()
            total_absences_period += (unjustified_abs + justified_abs)

            score_val = final_grade.final_score if final_grade else Decimal('1.00')
            
            # Homologar desempeño según escala institucional activa
            perf_level, is_approved = convert_score_to_performance_level(score_val, institution)

            if not is_approved:
                total_failed_count += 1

            total_weighted_score += score_val
            total_subjects_count += 1
            area_score_sum += score_val
            area_sub_count += 1

            subject_items.append({
                'subject': sub,
                'teacher': assignment.teacher if assignment else None,
                'criteria': criteria_details,
                'final_score': score_val,
                'performance_level': perf_level,
                'is_approved': is_approved,
                'unjustified_abs': unjustified_abs,
                'justified_abs': justified_abs,
                'feedback': " | ".join(feedback_notes) if feedback_notes else None,
            })

        if subject_items:
            area_avg = (area_score_sum / Decimal(str(area_sub_count))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            bulletin_areas.append({
                'area': area,
                'subjects': subject_items,
                'area_average': area_avg,
            })

    # Promedio general del estudiante en el periodo
    if total_subjects_count > 0:
        period_average = (total_weighted_score / Decimal(str(total_subjects_count))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    else:
        period_average = Decimal('1.00')

    # Desempeño del promedio general
    overall_performance, is_overall_approved = convert_score_to_performance_level(period_average, institution)

    # Cálculo del puesto (ranking) en la sección
    ranking_data = calculate_section_ranking(section, period)
    student_rank = ranking_data.get(student.id, {'rank': 1, 'total': len(ranking_data)})

    # Firma criptográfica inmutable
    verification_token = generate_bulletin_crypto_token(student.id, period.id, period_average, academic_year.year)
    
    # URL de verificación
    verification_url = f"https://academix.edu.co/verify/{verification_token}/"
    if request:
        try:
            verification_url = request.build_absolute_uri(f"/reports/verify/{verification_token}/")
        except Exception:
            pass

    qr_base64 = generate_bulletin_qr_base64(verification_url)

    # Estado de autorización de firma de la Rectora según bitácora de cierre
    from apps.rules.models import AcademicClosingLog
    closing_log = AcademicClosingLog.objects.filter(
        academic_period=period,
        closing_type=AcademicClosingLog.ClosingType.PERIOD
    ).order_by('-closed_at').first()
    rector_signature_authorized = closing_log.rector_signature_authorized if closing_log else True

    # Obtener el rector activo del sistema dinámicamente
    from apps.accounts.models import CustomUser
    rector_user = CustomUser.objects.filter(role=CustomUser.Role.RECTOR, is_active=True).order_by('-date_joined').first()
    if not rector_user:
        rector_user = CustomUser.objects.filter(role=CustomUser.Role.ADMIN, is_active=True).order_by('-date_joined').first()

    rector_name = rector_user.get_full_name() if rector_user else ""
    if not rector_name and rector_user:
        rector_name = rector_user.username.title()
    if not rector_name:
        rector_name = "Rector(a) Institucional"

    # Director de grupo asignado al curso
    group_director_name = ""
    if getattr(section, 'homeroom_teacher', None):
        group_director_name = section.homeroom_teacher.get_full_name() or section.homeroom_teacher.username
    elif group_director and getattr(group_director, 'user', None):
        group_director_name = group_director.user.get_full_name() or group_director.user.username
    if not group_director_name:
        group_director_name = "Director(a) de Grupo"

    return {
        'institution': institution,
        'student': student,
        'enrollment': enrollment,
        'section': section,
        'period': period,
        'academic_year': academic_year,
        'group_director': group_director,
        'group_director_name': group_director_name,
        'bulletin_areas': bulletin_areas,
        'period_average': period_average,
        'overall_performance': overall_performance,
        'is_overall_approved': is_overall_approved,
        'student_rank': student_rank['rank'],
        'total_students_section': student_rank['total'],
        'total_subjects_count': total_subjects_count,
        'total_failed_count': total_failed_count,
        'total_absences_period': total_absences_period,
        'rector_user': rector_user,
        'rector_name': rector_name,
        'rector_signature_authorized': rector_signature_authorized,
        'verification_token': verification_token,
        'verification_url': verification_url,
        'qr_base64': qr_base64,
        'issued_at': timezone.now(),
    }

def calculate_section_ranking(section, period):
    """
    Calcula los promedios de todos los alumnos de la sección en el periodo y asigna los puestos ordenados.
    """
    enrollments = Enrollment.objects.filter(
        course_section=section,
        academic_year=section.academic_year,
        status=Enrollment.Status.ACTIVE
    ).select_related('student')

    student_averages = []
    for enr in enrollments:
        grades = PeriodFinalGrade.objects.filter(
            student=enr.student,
            course_section=section,
            academic_period=period
        )
        if grades.exists():
            avg_score = sum([g.final_score for g in grades]) / Decimal(str(grades.count()))
            avg_dec = avg_score.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        else:
            avg_dec = Decimal('1.00')
        student_averages.append({
            'student_id': enr.student.id,
            'average': avg_dec
        })

    # Ordenar descendente por promedio
    student_averages.sort(key=lambda x: x['average'], reverse=True)

    ranking_map = {}
    total_count = len(student_averages)
    for idx, item in enumerate(student_averages, start=1):
        ranking_map[item['student_id']] = {
            'rank': idx,
            'total': total_count,
            'average': item['average']
        }

    return ranking_map

def build_section_consolidated_data(section, period):
    """
    Genera la sábana consolidada de calificaciones de todo el grupo para el periodo.
    """
    academic_year = section.academic_year
    enrollments = Enrollment.objects.filter(
        course_section=section,
        academic_year=academic_year,
        status=Enrollment.Status.ACTIVE
    ).select_related('student__user').order_by('student__user__last_name', 'student__user__first_name')

    # Asignaturas de la sección
    assignments = TeachingAssignment.objects.filter(
        course_section=section,
        academic_year=academic_year,
        is_active=True
    ).select_related('subject')
    subjects = list(dict.fromkeys([a.subject for a in assignments]))
    if not subjects:
        # Fallback a materias con notas en esta sección
        sub_ids = PeriodFinalGrade.objects.filter(course_section=section, academic_period=period).values_list('subject_id', flat=True).distinct()
        subjects = list(Subject.objects.filter(id__in=sub_ids).order_by('name'))

    ranking_map = calculate_section_ranking(section, period)

    rows = []
    for enr in enrollments:
        st = enr.student
        scores = {}
        scores_list = []
        failed_count = 0
        for sub in subjects:
            rec = PeriodFinalGrade.objects.filter(
                student=st,
                course_section=section,
                subject=sub,
                academic_period=period
            ).first()
            if rec:
                item_data = {
                    'subject': sub,
                    'score': rec.final_score,
                    'is_approved': rec.is_approved,
                    'badge': rec.badge_class
                }
                scores[sub.id] = item_data
                scores_list.append(item_data)
                if not rec.is_approved:
                    failed_count += 1
            else:
                item_data = {
                    'subject': sub,
                    'score': Decimal('1.00'),
                    'is_approved': False,
                    'badge': 'bg-danger text-white'
                }
                scores[sub.id] = item_data
                scores_list.append(item_data)
                failed_count += 1

        rank_info = ranking_map.get(st.id, {'rank': '-', 'average': Decimal('1.00')})
        rows.append({
            'student': st,
            'scores': scores,
            'scores_list': scores_list,
            'average': rank_info['average'],
            'rank': rank_info['rank'],
            'failed_count': failed_count,
        })

    # Ordenar filas por puesto
    rows.sort(key=lambda r: (r['rank'] if isinstance(r['rank'], int) else 999))

    return {
        'section': section,
        'period': period,
        'subjects': subjects,
        'rows': rows,
        'total_students': len(rows),
    }

def export_consolidated_csv(section, period):
    """
    Exporta la sábana consolidada en formato CSV con codificación UTF-8 con BOM.
    """
    data = build_section_consolidated_data(section, period)
    output = io.StringIO()
    # Escribir UTF-8 BOM
    output.write('\ufeff')
    writer = csv.writer(output, dialect='excel')

    # Encabezados
    headers = ['Puesto', 'Código Estudiantil', 'Apellidos y Nombres', 'Documento']
    for sub in data['subjects']:
        headers.append(f"{sub.code} ({sub.name})")
    headers.extend(['Promedio General', 'Asignaturas Reprobadas'])
    writer.writerow(headers)

    # Filas
    for row in data['rows']:
        st = row['student']
        line = [
            row['rank'],
            st.student_code,
            st.user.get_full_name() or st.user.username,
            st.user.document_number or ''
        ]
        for sub in data['subjects']:
            score_data = row['scores'].get(sub.id)
            line.append(str(score_data['score']) if score_data else '1.00')
        line.append(str(row['average']))
        line.append(row['failed_count'])
        writer.writerow(line)

    return output.getvalue()

def export_consolidated_excel(section, period):
    """
    Exporta la sábana consolidada en formato XLSX con openpyxl.
    Incluye estilos institucionales, colores por desempeño y autofit de columnas.
    Retorna bytes del archivo Excel.
    """
    try:
        import openpyxl
        from openpyxl.styles import (
            Font, PatternFill, Alignment, Border, Side, GradientFill
        )
        from openpyxl.utils import get_column_letter
    except ImportError:
        raise ImportError("Se requiere la librería 'openpyxl'. Instálala con: pip install openpyxl")

    data = build_section_consolidated_data(section, period)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"Consolidado {section.name[:25]}"

    # ── Paleta de colores institucional ──
    COLOR_HEADER_BG   = "0F172A"   # Azul oscuro
    COLOR_HEADER_FONT = "FFFFFF"
    COLOR_SUBHEADER   = "1E3A5F"
    COLOR_EXCEL_SUP   = "16A34A"   # Verde: Superior ≥ 4.6
    COLOR_EXCEL_ALTO  = "22C55E"   # Verde claro: Alto ≥ 4.0
    COLOR_EXCEL_BAS   = "F59E0B"   # Ámbar: Básico ≥ 3.0
    COLOR_EXCEL_BAJ   = "EF4444"   # Rojo: Bajo < 3.0
    COLOR_ALTERNADO   = "F1F5F9"   # Gris claro filas alternas
    COLOR_WHITE       = "FFFFFF"

    thin = Side(style='thin', color="CBD5E1")
    border_cell = Border(left=thin, right=thin, top=thin, bottom=thin)

    # ── Fila 1: Título institucional ──
    institution = get_institution_settings()
    ws.merge_cells(f"A1:{get_column_letter(4 + len(data['subjects']) + 1)}1")
    title_cell = ws['A1']
    title_cell.value = f"{institution.name.upper()} – SÁBANA CONSOLIDADA DE CALIFICACIONES"
    title_cell.font = Font(name='Calibri', bold=True, size=13, color=COLOR_HEADER_FONT)
    title_cell.fill = PatternFill('solid', fgColor=COLOR_HEADER_BG)
    title_cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    ws.row_dimensions[1].height = 24

    # ── Fila 2: Subtítulo sección y periodo ──
    ws.merge_cells(f"A2:{get_column_letter(4 + len(data['subjects']) + 1)}2")
    subtitle_cell = ws['A2']
    subtitle_cell.value = (
        f"Grupo: {section.name}  |  "
        f"Año Lectivo: {section.academic_year.year}  |  "
        f"Período: {period.name}  |  "
        f"Generado: {timezone.now().strftime('%d/%m/%Y %H:%M')}"
    )
    subtitle_cell.font = Font(name='Calibri', italic=True, size=10, color=COLOR_HEADER_FONT)
    subtitle_cell.fill = PatternFill('solid', fgColor=COLOR_SUBHEADER)
    subtitle_cell.alignment = Alignment(horizontal='center', vertical='center')
    ws.row_dimensions[2].height = 18

    # ── Fila 3: Encabezados de columnas ──
    header_style = Font(name='Calibri', bold=True, size=10, color=COLOR_HEADER_FONT)
    header_fill  = PatternFill('solid', fgColor=COLOR_SUBHEADER)
    header_align = Alignment(horizontal='center', vertical='center', wrap_text=True)

    headers = ['#', 'Código', 'Apellidos y Nombres', 'Documento']
    for sub in data['subjects']:
        headers.append(f"{sub.code}\n{sub.name[:18]}")
    headers.extend(['Promedio', 'Reprobadas'])

    for col_idx, header in enumerate(headers, start=1):
        cell = ws.cell(row=3, column=col_idx, value=header)
        cell.font = header_style
        cell.fill = header_fill
        cell.alignment = header_align
        cell.border = border_cell
    ws.row_dimensions[3].height = 36

    # ── Filas de datos ──
    def score_fill(score_val):
        """Devuelve un PatternFill basado en la nota."""
        sc = float(score_val)
        if sc >= 4.6:
            return PatternFill('solid', fgColor=COLOR_EXCEL_SUP)
        elif sc >= 4.0:
            return PatternFill('solid', fgColor=COLOR_EXCEL_ALTO)
        elif sc >= 3.0:
            return PatternFill('solid', fgColor=COLOR_EXCEL_BAS)
        else:
            return PatternFill('solid', fgColor=COLOR_EXCEL_BAJ)

    def score_font(score_val):
        sc = float(score_val)
        color = COLOR_WHITE if sc < 3.0 or sc >= 4.6 else "000000"
        return Font(name='Calibri', size=10, bold=(sc < 3.0), color=color)

    for row_idx, row in enumerate(data['rows'], start=4):
        alt_fill = PatternFill('solid', fgColor=(COLOR_ALTERNADO if row_idx % 2 == 0 else COLOR_WHITE))
        st = row['student']
        base_cells = [
            row['rank'],
            st.student_code,
            st.user.get_full_name() or st.user.username,
            st.user.document_number or '',
        ]
        for col_idx, val in enumerate(base_cells, start=1):
            cell = ws.cell(row=row_idx, column=col_idx, value=val)
            cell.font = Font(name='Calibri', size=10)
            cell.fill = alt_fill
            cell.alignment = Alignment(horizontal='center' if col_idx in [1, 2, 4] else 'left', vertical='center')
            cell.border = border_cell

        # Notas por asignatura
        for sub_idx, sub in enumerate(data['subjects'], start=5):
            score_data = row['scores'].get(sub.id)
            sc = score_data['score'] if score_data else Decimal('1.00')
            cell = ws.cell(row=row_idx, column=sub_idx, value=float(sc))
            cell.number_format = '0.00'
            cell.fill = score_fill(sc)
            cell.font = score_font(sc)
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = border_cell

        # Promedio y reprobadas
        avg_col = 5 + len(data['subjects'])
        avg_cell = ws.cell(row=row_idx, column=avg_col, value=float(row['average']))
        avg_cell.number_format = '0.00'
        avg_cell.fill = score_fill(row['average'])
        avg_cell.font = score_font(row['average'])
        avg_cell.alignment = Alignment(horizontal='center', vertical='center')
        avg_cell.border = border_cell

        rep_col = avg_col + 1
        rep_cell = ws.cell(row=row_idx, column=rep_col, value=row['failed_count'])
        rep_fill = PatternFill('solid', fgColor=COLOR_EXCEL_BAJ) if row['failed_count'] > 0 else alt_fill
        rep_font_color = COLOR_WHITE if row['failed_count'] > 0 else '000000'
        rep_cell.fill = rep_fill
        rep_cell.font = Font(name='Calibri', size=10, bold=(row['failed_count'] > 0), color=rep_font_color)
        rep_cell.alignment = Alignment(horizontal='center', vertical='center')
        rep_cell.border = border_cell
        ws.row_dimensions[row_idx].height = 16

    # ── Autofit de columnas ──
    ws.column_dimensions['A'].width = 5
    ws.column_dimensions['B'].width = 14
    ws.column_dimensions['C'].width = 30
    ws.column_dimensions['D'].width = 14
    for i, sub in enumerate(data['subjects'], start=5):
        col_letter = get_column_letter(i)
        ws.column_dimensions[col_letter].width = max(10, min(len(sub.name), 18))
    avg_letter = get_column_letter(5 + len(data['subjects']))
    ws.column_dimensions[avg_letter].width = 10
    ws.column_dimensions[get_column_letter(6 + len(data['subjects']))].width = 10

    # ── Fila de leyenda de desempeños ──
    leyenda_row = 4 + len(data['rows']) + 1
    ws.cell(row=leyenda_row, column=1, value='LEYENDA:').font = Font(bold=True, size=9)
    legend_items = [
        ('≥ 4.6 Superior', COLOR_EXCEL_SUP, COLOR_WHITE),
        ('≥ 4.0 Alto', COLOR_EXCEL_ALTO, '000000'),
        ('≥ 3.0 Básico', COLOR_EXCEL_BAS, '000000'),
        ('< 3.0 Bajo', COLOR_EXCEL_BAJ, COLOR_WHITE),
    ]
    for li_idx, (label, bg, fg) in enumerate(legend_items, start=2):
        c = ws.cell(row=leyenda_row, column=li_idx, value=label)
        c.fill = PatternFill('solid', fgColor=bg)
        c.font = Font(size=9, color=fg)
        c.alignment = Alignment(horizontal='center')

    # ── Congelar encabezado ──
    ws.freeze_panes = 'A4'

    # Serializar a bytes
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return output.getvalue()


def build_certificate_data(student, certificate_type='ESTUDIO', academic_year=None, request=None):
    """
    Construye los datos para generar una Constancia o Certificado de Estudio oficial.
    Tipos soportados:
      - ESTUDIO: Constancia básica de que el estudiante pertenece a la institución.
      - RENDIMIENTO: Certificado con promedio general del año.
      - MATRICULA: Certificado de matrícula activa (inicio de año).
    Incluye código único de verificación QR.
    """
    institution = get_institution_settings()
    if academic_year is None:
        from apps.courses.services import get_current_academic_year
        academic_year = get_current_academic_year()

    enrollment = None
    section = None
    if academic_year:
        enrollment = Enrollment.objects.filter(
            student=student,
            academic_year=academic_year,
            status=Enrollment.Status.ACTIVE
        ).select_related('course_section__grade_level').first()
        if enrollment:
            section = enrollment.course_section

    # Calcular promedio anual si es RENDIMIENTO
    annual_average = None
    if certificate_type == 'RENDIMIENTO' and academic_year:
        from apps.grades.models import PeriodFinalGrade
        grades_qs = PeriodFinalGrade.objects.filter(
            student=student,
            course_section=section,
            academic_period__academic_year=academic_year
        ) if section else PeriodFinalGrade.objects.none()
        if grades_qs.exists():
            total = sum(g.final_score for g in grades_qs)
            annual_average = (total / Decimal(str(grades_qs.count()))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    # Generar token único de verificación
    secret = getattr(settings, 'SECRET_KEY', 'academix-critical-key-2026')
    payload = f"CERT|STUDENT:{student.id}|TYPE:{certificate_type}|YEAR:{academic_year.year if academic_year else 'N/A'}|TS:{timezone.now().strftime('%Y%m%d')}"
    raw_token = hmac.new(secret.encode('utf-8'), payload.encode('utf-8'), hashlib.sha256).hexdigest()
    cert_token = raw_token[:16].upper()

    verification_url = f"https://academix.edu.co/verify/cert/{cert_token}/"
    if request:
        try:
            verification_url = request.build_absolute_uri(f"/reports/verify/{cert_token}/")
        except Exception:
            pass

    qr_base64 = generate_bulletin_qr_base64(verification_url)

    certificate_type_labels = {
        'ESTUDIO': 'CONSTANCIA DE ESTUDIO',
        'RENDIMIENTO': 'CERTIFICADO DE RENDIMIENTO ACADÉMICO',
        'MATRICULA': 'CERTIFICADO DE MATRÍCULA',
    }

    return {
        'institution': institution,
        'student': student,
        'enrollment': enrollment,
        'section': section,
        'academic_year': academic_year,
        'certificate_type': certificate_type,
        'certificate_type_label': certificate_type_labels.get(certificate_type, 'CONSTANCIA'),
        'annual_average': annual_average,
        'cert_token': cert_token,
        'verification_url': verification_url,
        'qr_base64': qr_base64,
        'issued_at': timezone.now(),
        'issued_date_str': timezone.now().strftime('%d de %B de %Y'),
    }


def build_honor_roll_data(section, period):
    """
    Genera el Cuadro de Honor (Top 5 estudiantes) y estadísticas generales de aprobación.
    """
    consolidated = build_section_consolidated_data(section, period)
    rows = consolidated['rows']

    # Top 5 con promedios >= 3.80
    honor_students = [r for r in rows if r['average'] >= Decimal('3.80')][:5]

    total = len(rows)
    passed_all = len([r for r in rows if r['failed_count'] == 0])
    passed_rate = ((Decimal(str(passed_all)) / Decimal(str(total))) * Decimal('100.00')).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP) if total > 0 else Decimal('0.0')

    # Detección de asignaturas críticas (con mayor número de reprobados)
    subject_failed_counts = {}
    for sub in consolidated['subjects']:
        failed_in_sub = sum([1 for r in rows if not r['scores'].get(sub.id, {}).get('is_approved', True)])
        subject_failed_counts[sub] = failed_in_sub

    critical_subjects = sorted(subject_failed_counts.items(), key=lambda x: x[1], reverse=True)[:3]

    return {
        'section': section,
        'period': period,
        'honor_students': honor_students,
        'total_students': total,
        'passed_all_count': passed_all,
        'approval_rate': passed_rate,
        'critical_subjects': critical_subjects,
    }
