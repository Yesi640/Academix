from django.test import TestCase
from datetime import date
from .models import AcademicYear, GradeLevel, CourseSection
from .services import set_current_academic_year, create_course_section

class CoursesTests(TestCase):
    def setUp(self):
        self.year2025 = AcademicYear.objects.create(
            year=2025,
            name='Año Escolar 2025',
            start_date=date(2025, 1, 15),
            end_date=date(2025, 11, 30),
            status=AcademicYear.Status.CLOSED,
            is_current=False
        )
        self.year2026 = AcademicYear.objects.create(
            year=2026,
            name='Año Escolar 2026',
            start_date=date(2026, 1, 15),
            end_date=date(2026, 11, 30),
            status=AcademicYear.Status.PLANNING,
            is_current=False
        )
        self.grade6 = GradeLevel.objects.create(
            name='Sexto',
            code='06',
            level_stage=GradeLevel.LevelStage.SECUNDARIA,
            order=6
        )

    def test_set_current_academic_year_exclusivity(self):
        # Marcar 2025 como actual
        set_current_academic_year(self.year2025.id)
        self.year2025.refresh_from_db()
        self.assertTrue(self.year2025.is_current)

        # Ahora marcar 2026 como actual, 2025 debe perder el flag
        set_current_academic_year(self.year2026.id)
        self.year2025.refresh_from_db()
        self.year2026.refresh_from_db()

        self.assertFalse(self.year2025.is_current)
        self.assertTrue(self.year2026.is_current)
        self.assertEqual(self.year2026.status, AcademicYear.Status.ACTIVE)

    def test_create_section_service(self):
        section = create_course_section(
            academic_year=self.year2026,
            grade_level=self.grade6,
            name='6-A',
            classroom='Aula 101',
            capacity=35
        )
        self.assertEqual(section.name, '6-A')
        self.assertEqual(section.academic_year, self.year2026)
        self.assertEqual(section.grade_level, self.grade6)

    def test_create_academic_year_validation_and_features(self):
        """Prueba creación de año lectivo desde 2026 y rechazo de años anteriores."""
        from .services import create_academic_year
        # Año inferior a 2026 debe lanzar error
        with self.assertRaises(ValueError):
            create_academic_year(year=2024)

        # Año 2027 válido con periodos estándar automáticos
        year2027 = create_academic_year(
            year=2027,
            name='Año Escolar 2027',
            is_current=True,
            auto_create_periods=True,
            auto_generate_sections=False
        )
        self.assertEqual(year2027.year, 2027)
        self.assertTrue(year2027.is_current)
        self.assertEqual(year2027.periods.count(), 4)

    def test_ensure_standard_colegio_grades_and_sections(self):
        """Prueba catálogo de grados según alcance de colegio (Primaria, Secundaria, Completa)."""
        from .models import InstitutionSetting
        from .services import ensure_standard_colegio_grades, generate_default_sections_for_year

        # 1. Solo Primaria
        prim_grades = ensure_standard_colegio_grades(InstitutionSetting.SchoolLevelScope.PRIMARIA)
        self.assertTrue(any(g.name == 'Primero' for g in prim_grades))
        self.assertFalse(any(g.name == 'Once' for g in prim_grades))

        # 2. Solo Secundaria
        sec_grades = ensure_standard_colegio_grades(InstitutionSetting.SchoolLevelScope.SECUNDARIA)
        self.assertTrue(any(g.name == 'Once' for g in sec_grades))
        self.assertFalse(any(g.name == 'Primero' for g in sec_grades))

        # 3. Completa
        all_grades = ensure_standard_colegio_grades(InstitutionSetting.SchoolLevelScope.COMPLETA)
        self.assertEqual(len(all_grades), 12)  # Transición a 11°

        # 4. Generación de cursos típicos
        sections = generate_default_sections_for_year(self.year2026, scope=InstitutionSetting.SchoolLevelScope.COMPLETA)
        self.assertEqual(len(sections), 12)
