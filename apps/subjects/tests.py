from decimal import Decimal
from django.test import TestCase
from .models import KnowledgeArea, Subject, GradeSubject
from apps.courses.models import GradeLevel
from .services import configure_grade_subject

class SubjectsTests(TestCase):
    def setUp(self):
        self.area = KnowledgeArea.objects.create(name='Matemáticas', order=1)
        self.subject = Subject.objects.create(
            area=self.area,
            name='Álgebra',
            code='MAT-ALG'
        )
        self.grade = GradeLevel.objects.create(
            name='Octavo',
            code='08',
            level_stage=GradeLevel.LevelStage.SECUNDARIA,
            order=8
        )

    def test_grade_subject_configuration(self):
        gs = configure_grade_subject(
            grade_level=self.grade,
            subject=self.subject,
            weekly_hours=5,
            weight_percentage=Decimal('100.00')
        )
        self.assertEqual(gs.weekly_hours, 5)
        self.assertEqual(gs.weight_percentage, Decimal('100.00'))
        self.assertEqual(GradeSubject.objects.count(), 1)

    def test_decimal_precision(self):
        gs = configure_grade_subject(
            grade_level=self.grade,
            subject=self.subject,
            weekly_hours=4,
            weight_percentage=Decimal('60.50')
        )
        self.assertIsInstance(gs.weight_percentage, Decimal)
        self.assertEqual(gs.weight_percentage, Decimal('60.50'))


class SubjectRAPCurriculumTests(TestCase):
    """
    Pruebas para la estructura curricular por RAPs (Resultados de Aprendizaje)
    conforme al esquema pedagógico del cliente (Área -> Materia -> Indicadores -> RAPs con Saber, Hacer, Ser y Evidencias).
    """
    def setUp(self):
        self.area = KnowledgeArea.objects.create(name='Ciencias Naturales', order=2)
        self.subject = Subject.objects.create(
            area=self.area,
            name='Química Orgánica',
            code='QUI-ORG'
        )

    def test_create_complete_rap(self):
        from .models import SubjectNorm
        rap = SubjectNorm.objects.create(
            subject=self.subject,
            code='QUI-RAP1',
            title='Estructura del Carbono e Hibridación',
            description='Explica los tipos de enlace y geometría del carbono.',
            competency='Modelación de estructuras moleculares y transformaciones químicas.',
            domain='Cognitivo y Experimental',
            dimension='Pensamiento Científico',
            indicator='Diferencia enlaces sp, sp2 y sp3 y dibuja geometrías moleculares.',
            saber='Configuración electrónica del carbono, orbitales moleculares y tetravalencia.',
            hacer='Construye modelos tridimensionales de hidrocarburos.',
            ser='Rigurosidad técnica y trabajo cooperativo en el laboratorio.',
            evidence='Informe de modelación molecular y reporte de laboratorio.',
            order=1
        )
        self.assertEqual(rap.rap_label, 'RAP 1')
        self.assertEqual(rap.competency, 'Modelación de estructuras moleculares y transformaciones químicas.')
        self.assertEqual(rap.domain, 'Cognitivo y Experimental')
        self.assertEqual(rap.dimension, 'Pensamiento Científico')
        self.assertTrue(rap.saber.startswith('Configuración'))
        self.assertTrue(rap.hacer.startswith('Construye'))
        self.assertTrue(rap.ser.startswith('Rigurosidad'))
        self.assertTrue(rap.evidence.startswith('Informe'))

    def test_criteria_generation_from_subject_raps(self):
        from .models import SubjectNorm
        from apps.grades.services import get_or_create_default_criteria
        from apps.courses.models import CourseSection, AcademicYear
        from apps.periods.models import AcademicPeriod
        from datetime import date

        # Crear 3 RAPs
        for i in range(1, 4):
            SubjectNorm.objects.create(
                subject=self.subject,
                code=f'QUI-RAP{i}',
                title=f'Resultado de Aprendizaje {i}',
                indicator=f'Indicador de logro {i}',
                saber=f'Saber conceptual {i}',
                hacer=f'Hacer procedimental {i}',
                ser=f'Ser actitudinal {i}',
                evidence=f'Evidencia de elaboración {i}',
                order=i
            )

        year = AcademicYear.objects.create(year=2026, name='2026', start_date=date(2026, 1, 15), end_date=date(2026, 11, 30))
        grade = GradeLevel.objects.create(name='Décimo', code='10', order=10)
        section = CourseSection.objects.create(academic_year=year, grade_level=grade, name='10-B')
        period = AcademicPeriod.objects.create(academic_year=year, number=1, name='Periodo 1', start_date=date(2026, 1, 15), end_date=date(2026, 4, 1), percentage=Decimal('25.00'))

        criteria = get_or_create_default_criteria(section, self.subject, period)
        self.assertEqual(len(criteria), 3)
        self.assertEqual(criteria[0].norm.order, 1)
        self.assertEqual(criteria[0].name, 'RAP 1: Resultado de Aprendizaje 1')
        self.assertEqual(criteria[0].topic, 'Evidencia de elaboración 1')
        self.assertEqual(sum(c.percentage for c in criteria), Decimal('100.00'))

