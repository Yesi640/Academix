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


class HybridInstitutionParametrizationTests(TestCase):
    """
    Pruebas unitarias para el Pilar 1: Motor de Parametrización Institucional (SaaS Híbrido Público/Privado).
    """
    def setUp(self):
        from decimal import Decimal
        from django.test import RequestFactory
        from .models import InstitutionSetting
        self.factory = RequestFactory()
        self.setting = InstitutionSetting.get_settings()
        self.setting.sector_mode = InstitutionSetting.SectorMode.PRIVATE
        self.setting.enable_tuition_billing = True
        self.setting.block_report_cards_on_debt = True
        self.setting.grading_scale_type = InstitutionSetting.GradingScaleType.NUMERIC_5
        self.setting.min_grade = Decimal('1.00')
        self.setting.max_grade = Decimal('5.00')
        self.setting.passing_grade = Decimal('3.00')
        self.setting.save()

    def test_switch_to_public_mode_preset(self):
        """Al conmutar a público, se activan gratuidad, PAE y SIMAT, y se desactiva retención de boletines."""
        self.setting.apply_sector_preset(self.setting.SectorMode.PUBLIC)
        self.setting.refresh_from_db()

        self.assertTrue(self.setting.is_public_institution)
        self.assertFalse(self.setting.is_private_institution)
        self.assertTrue(self.setting.enable_gratuity_control)
        self.assertTrue(self.setting.enable_pae_module)
        self.assertTrue(self.setting.enable_simat_integration)
        self.assertFalse(self.setting.enable_tuition_billing)
        self.assertFalse(self.setting.allows_report_card_debt_blocking)

    def test_public_institution_cannot_block_report_cards(self):
        """Por ley y constitución, un colegio público nunca puede tener activo el bloqueo de notas por deudas."""
        self.setting.sector_mode = self.setting.SectorMode.PUBLIC
        self.setting.block_report_cards_on_debt = True
        self.setting.clean()
        self.assertFalse(self.setting.block_report_cards_on_debt)
        self.assertFalse(self.setting.allows_report_card_debt_blocking)

    def test_performance_level_conversion_numeric_5(self):
        """Conversión de escala 1.0 - 5.0 a niveles MEN (Bajo, Básico, Alto, Superior)."""
        from .services import convert_score_to_performance_level
        self.setting.grading_scale_type = self.setting.GradingScaleType.NUMERIC_5
        self.setting.save()

        level, approved = convert_score_to_performance_level('2.80', self.setting)
        self.assertEqual(level, 'BAJO')
        self.assertFalse(approved)

        level, approved = convert_score_to_performance_level('3.50', self.setting)
        self.assertEqual(level, 'BASICO')
        self.assertTrue(approved)

        level, approved = convert_score_to_performance_level('4.20', self.setting)
        self.assertEqual(level, 'ALTO')
        self.assertTrue(approved)

        level, approved = convert_score_to_performance_level('4.80', self.setting)
        self.assertEqual(level, 'SUPERIOR')
        self.assertTrue(approved)

    def test_performance_level_conversion_numeric_100(self):
        """Conversión de escala 0 - 100 a niveles MEN."""
        from .services import convert_score_to_performance_level
        self.setting.grading_scale_type = self.setting.GradingScaleType.NUMERIC_100
        self.setting.passing_grade = 60
        self.setting.save()

        level, approved = convert_score_to_performance_level('55.00', self.setting)
        self.assertEqual(level, 'BAJO')
        self.assertFalse(approved)

        level, approved = convert_score_to_performance_level('85.00', self.setting)
        self.assertEqual(level, 'ALTO')
        self.assertTrue(approved)

    def test_score_validation(self):
        """Valida que una nota fuera de los límites de la institución sea rechazada."""
        from django.core.exceptions import ValidationError
        from .services import validate_score_input
        self.setting.min_grade = 1
        self.setting.max_grade = 5
        self.setting.save()

        # Nota válida
        val = validate_score_input('4.5', self.setting)
        self.assertEqual(val, 4.5)

        # Nota fuera de rango superior
        with self.assertRaises(ValidationError):
            validate_score_input('6.0', self.setting)

        # Nota fuera de rango inferior
        with self.assertRaises(ValidationError):
            validate_score_input('0.5', self.setting)

    def test_decorators_hybrid_access_control(self):
        """Prueba decoradores @require_public_school y @require_private_school."""
        from django.core.exceptions import PermissionDenied
        from django.http import HttpResponse
        from .decorators import require_public_school, require_private_school

        @require_public_school
        def pae_view(request):
            return HttpResponse("PAE")

        @require_private_school
        def billing_view(request):
            return HttpResponse("Facturacion")

        req = self.factory.get('/')

        # 1. Configuración en PRIVADO
        self.setting.apply_sector_preset(self.setting.SectorMode.PRIVATE)
        resp = billing_view(req)
        self.assertEqual(resp.status_code, 200)

        with self.assertRaises(PermissionDenied):
            pae_view(req)

        # 2. Conmutar a PUBLICO
        self.setting.apply_sector_preset(self.setting.SectorMode.PUBLIC)
        resp_pae = pae_view(req)
        self.assertEqual(resp_pae.status_code, 200)

        with self.assertRaises(PermissionDenied):
            billing_view(req)

