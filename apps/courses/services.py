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

