import datetime
from django.db import transaction
from .models import AcademicYear, CourseSection, GradeLevel, InstitutionSetting
from apps.audit.services import log_audit

def get_current_academic_year():
    """Retorna el año lectivo vigente actual o None si no hay ninguno marcado."""
    return AcademicYear.objects.filter(is_current=True).first() or AcademicYear.objects.filter(status=AcademicYear.Status.ACTIVE).first()

@transaction.atomic
def set_current_academic_year(year_id, user=None):
    """
    Establece de manera atómica el año lectivo activo en el sistema,
    desactivando los restantes y auditando el cambio.
    """
    target_year = AcademicYear.objects.select_for_update().get(id=year_id)
    
    # Desmarcar los demás
    AcademicYear.objects.exclude(id=target_year.id).filter(is_current=True).update(is_current=False)
    
    target_year.is_current = True
    target_year.status = AcademicYear.Status.ACTIVE
    target_year.save(update_fields=['is_current', 'status'])

    log_audit(
        action='UPDATE',
        table_name='AcademicYear',
        record_id=target_year.id,
        new_values={'year': target_year.year, 'is_current': True, 'status': target_year.status},
        reason=f'Establecido año {target_year.year} como año lectivo vigente',
        user=user
    )

    return target_year

# Catálogo oficial de grados de un colegio regular colombiano
COLEGIO_GRADES_CATALOG = [
    # Preescolar
    ('Transición', 'GR-00', GradeLevel.LevelStage.PREESCOLAR, 0),
    # Básica Primaria
    ('Primero', 'GR-01', GradeLevel.LevelStage.PRIMARIA, 1),
    ('Segundo', 'GR-02', GradeLevel.LevelStage.PRIMARIA, 2),
    ('Tercero', 'GR-03', GradeLevel.LevelStage.PRIMARIA, 3),
    ('Cuarto', 'GR-04', GradeLevel.LevelStage.PRIMARIA, 4),
    ('Quinto', 'GR-05', GradeLevel.LevelStage.PRIMARIA, 5),
    # Básica Secundaria
    ('Sexto', 'GR-06', GradeLevel.LevelStage.SECUNDARIA, 6),
    ('Séptimo', 'GR-07', GradeLevel.LevelStage.SECUNDARIA, 7),
    ('Octavo', 'GR-08', GradeLevel.LevelStage.SECUNDARIA, 8),
    ('Noveno', 'GR-09', GradeLevel.LevelStage.SECUNDARIA, 9),
    # Educación Media
    ('Décimo', 'GR-10', GradeLevel.LevelStage.MEDIA, 10),
    ('Once', 'GR-11', GradeLevel.LevelStage.MEDIA, 11),
]

def ensure_standard_colegio_grades(scope=InstitutionSetting.SchoolLevelScope.COMPLETA):
    """
    Crea o sincroniza los grados estándar de colegio según el alcance institucional:
    - PRIMARIA: Transición y 1° a 5°
    - SECUNDARIA: 6° a 11°
    - COMPLETA: Transición a 11°
    """
    inst_type = InstitutionSetting.InstitutionType.COLEGIO

    if scope == InstitutionSetting.SchoolLevelScope.PRIMARIA:
        allowed_stages = [GradeLevel.LevelStage.PREESCOLAR, GradeLevel.LevelStage.PRIMARIA]
    elif scope == InstitutionSetting.SchoolLevelScope.SECUNDARIA:
        allowed_stages = [GradeLevel.LevelStage.SECUNDARIA, GradeLevel.LevelStage.MEDIA]
    else:
        allowed_stages = [
            GradeLevel.LevelStage.PREESCOLAR,
            GradeLevel.LevelStage.PRIMARIA,
            GradeLevel.LevelStage.SECUNDARIA,
            GradeLevel.LevelStage.MEDIA,
        ]

    created_or_found = []
    for name, code, stage, order in COLEGIO_GRADES_CATALOG:
        if stage in allowed_stages:
            g, _ = GradeLevel.objects.get_or_create(
                institution_type=inst_type,
                code=code,
                defaults={'name': name, 'level_stage': stage, 'order': order}
            )
            created_or_found.append(g)

    return created_or_found

@transaction.atomic
def generate_default_sections_for_year(academic_year, scope=None, user=None):
    """
    Genera automáticamente los cursos/salones normales de un colegio para el año lectivo dado.
    Ejemplo: Transición A, 1°A, 2°A... 11°A
    """
    settings_obj = InstitutionSetting.get_settings()
    if scope is None:
        scope = settings_obj.school_scope

    grades = ensure_standard_colegio_grades(scope)
    sections_created = []

    for g in grades:
        if g.order == 0:
            sec_name = "Transición A"
            classroom = "Aula Preescolar 1"
        elif g.order <= 5:
            sec_name = f"{g.order}°A"
            classroom = f"Aula Primaria {g.order}01"
        else:
            sec_name = f"{g.order}-A"
            classroom = f"Aula Secundaria {g.order}01"

        sec, created = CourseSection.objects.get_or_create(
            academic_year=academic_year,
            grade_level=g,
            name=sec_name,
            defaults={'classroom': classroom, 'capacity': 35}
        )
        if created:
            sections_created.append(sec)

    return sections_created

@transaction.atomic
def create_academic_year(year, name=None, start_date=None, end_date=None, is_current=False,
                         auto_create_periods=True, auto_generate_sections=False, user=None):
    """
    Crea un nuevo año lectivo (permitido desde 2026 en adelante).
    Opcionalmente configura los periodos lectivos y los cursos sugeridos.
    """
    year = int(year)
    if year < 2026:
        raise ValueError("El año lectivo debe ser igual o superior a 2026.")

    if not name:
        name = f"Año Escolar {year}"
    if not start_date:
        start_date = datetime.date(year, 1, 15)
    if not end_date:
        end_date = datetime.date(year, 11, 30)

    # Validar que no exista
    if AcademicYear.objects.filter(year=year).exists():
        raise ValueError(f"El año lectivo {year} ya existe en el sistema.")

    status = AcademicYear.Status.ACTIVE if is_current else AcademicYear.Status.PLANNING

    academic_year = AcademicYear.objects.create(
        year=year,
        name=name,
        start_date=start_date,
        end_date=end_date,
        status=status,
        is_current=False
    )

    if is_current:
        academic_year = set_current_academic_year(academic_year.id, user=user)

    if auto_create_periods:
        from apps.periods.services import create_standard_periods
        create_standard_periods(academic_year, user=user)

    if auto_generate_sections:
        generate_default_sections_for_year(academic_year, user=user)

    log_audit(
        action='INSERT',
        table_name='AcademicYear',
        record_id=academic_year.id,
        new_values={'year': year, 'name': name, 'is_current': is_current},
        reason=f'Creación de nuevo año lectivo {year}',
        user=user
    )

    return academic_year

@transaction.atomic
def create_course_section(academic_year, grade_level, name, classroom='', homeroom_teacher=None, capacity=35, user=None):
    """
    Crea un nuevo grupo o sección escolar garantizando unicidad y trazabilidad.
    """
    section = CourseSection.objects.create(
        academic_year=academic_year,
        grade_level=grade_level,
        name=name,
        classroom=classroom,
        homeroom_teacher=homeroom_teacher,
        capacity=capacity
    )

    log_audit(
        action='INSERT',
        table_name='CourseSection',
        record_id=section.id,
        new_values={
            'name': section.name,
            'year': academic_year.year,
            'grade': grade_level.name,
            'capacity': capacity
        },
        reason=f'Creación de sección académica {name}',
        user=user
    )

    return section


# ══════════════════════════════════════════════════════════════════════════════
# PILAR 1: MOTOR DE PARAMETRIZACIÓN INSTITUCIONAL (SAAS HÍBRIDO PÚBLICO/PRIVADO)
# ══════════════════════════════════════════════════════════════════════════════

def get_institution_settings():
    """
    Selector centralizado para recuperar la parametrización institucional activa.
    Singleton garantizado.
    """
    return InstitutionSetting.get_settings()


def is_public_school_mode():
    """Retorna True si la institución opera bajo el régimen oficial / público (gratuidad)."""
    return get_institution_settings().is_public_institution


def is_private_school_mode():
    """Retorna True si la institución opera bajo el régimen privado / no oficial."""
    return get_institution_settings().is_private_institution


def get_grading_scale_config():
    """
    Retorna la configuración completa del sistema de evaluación activo.
    """
    setting = get_institution_settings()
    return {
        'scale_type': setting.grading_scale_type,
        'min_grade': setting.min_grade,
        'max_grade': setting.max_grade,
        'passing_grade': setting.passing_grade,
        'decimal_places': setting.grade_decimal_places,
        'period_structure': setting.period_structure,
    }


def convert_score_to_performance_level(score, setting=None):
    """
    Convierte cualquier puntaje cuantitativo (ej. 3.8 en 5.0, 78 en 100, 7.5 en 10)
    al nivel de desempeño oficial del MEN (Decreto 1290):
    - SUPERIOR
    - ALTO
    - BASICO
    - BAJO
    """
    from decimal import Decimal
    if setting is None:
        setting = get_institution_settings()

    if score is None:
        return 'BAJO', False

    try:
        score_dec = Decimal(str(score))
    except Exception:
        return 'BAJO', False

    scale = setting.grading_scale_type
    passing = setting.passing_grade

    is_approved = score_dec >= passing

    if scale == InstitutionSetting.GradingScaleType.NUMERIC_100:
        if score_dec < Decimal('60.00'):
            return 'BAJO', False
        elif score_dec < Decimal('80.00'):
            return 'BASICO', True
        elif score_dec < Decimal('95.00'):
            return 'ALTO', True
        else:
            return 'SUPERIOR', True

    elif scale == InstitutionSetting.GradingScaleType.NUMERIC_10:
        if score_dec < Decimal('6.00'):
            return 'BAJO', False
        elif score_dec < Decimal('8.00'):
            return 'BASICO', True
        elif score_dec < Decimal('9.20'):
            return 'ALTO', True
        else:
            return 'SUPERIOR', True

    else:
        # NUMERIC_5 o CONCEPTUAL_MEN (1.00 a 5.00 estándar oficial colombiano)
        if score_dec < Decimal('3.00'):
            return 'BAJO', False
        elif score_dec < Decimal('4.00'):
            return 'BASICO', True
        elif score_dec < Decimal('4.60'):
            return 'ALTO', True
        else:
            return 'SUPERIOR', True


def validate_score_input(score, setting=None):
    """
    Valida si una calificación numérica respeta los límites establecidos en la configuración del colegio.
    Lanza ValidationError en caso de estar fuera de límites.
    """
    from decimal import Decimal
    from django.core.exceptions import ValidationError

    if setting is None:
        setting = get_institution_settings()

    if score is None or str(score).strip() == '':
        return None

    try:
        val = Decimal(str(score).strip().replace(',', '.'))
    except Exception:
        raise ValidationError(f"Valor numérico no válido: {score}")

    if val < setting.min_grade or val > setting.max_grade:
        raise ValidationError(
            f"La calificación debe encontrarse entre {setting.min_grade} y {setting.max_grade} según la escala activa de la institución."
        )

    return val


def is_feature_active(feature_flag_name):
    """
    Evalúa si un módulo o característica específica está activa en la parametrización institucional.
    Ej: 'enable_pae_module', 'enable_tuition_billing', 'enable_simat_integration'
    """
    setting = get_institution_settings()
    return bool(getattr(setting, feature_flag_name, False))


def can_download_report_card(student_profile):
    """
    Pilar 1 y 2: Regla de negocio de acceso a boletines de notas.
    - Colegio Público: El acceso es universal e incondicional (no existe cobro ni retención legal).
    - Colegio Privado: Si está habilitado el bloqueo por morosidad, valida estados de cuenta pendientes.
    Retorna tupla: (puede_descargar: bool, motivo: str)
    """
    setting = get_institution_settings()

    # Si es institución pública, NUNCA se bloquea por causales económicas
    if setting.is_public_institution:
        return True, "Acceso concedido bajo principio de gratuidad universal oficial (Colegio Público)."

    # Si es institución privada pero no tiene activada la retención de boletines
    if not setting.allows_report_card_debt_blocking:
        return True, "Descarga de boletín habilitada institucionalmente."

    # Si es privada y tiene activado el bloqueo, verificar deudas del estudiante/familia
    # Se consulta si existe un modelo de cartera/pagos con morosidad
    try:
        if hasattr(student_profile, 'has_financial_debt') and student_profile.has_financial_debt():
            return False, "La descarga del boletín se encuentra suspendida temporalmente por obligaciones financieras pendientes."
    except Exception:
        pass

    return True, "Paz y salvo financiero verificado."


@transaction.atomic
def apply_institution_mode(sector_mode, user=None):
    """
    Conmuta en caliente el modo del SaaS entre Público y Privado y audita el evento.
    """
    setting = get_institution_settings()
    old_sector = setting.sector_mode

    setting.apply_sector_preset(sector_mode)

    log_audit(
        action='CONFIG_CHANGE',
        table_name='InstitutionSetting',
        record_id=setting.id,
        old_values={'sector_mode': old_sector},
        new_values={'sector_mode': sector_mode},
        reason=f"Cambio de régimen institucional a {sector_mode} (SaaS Híbrido)",
        user=user
    )

    return setting


