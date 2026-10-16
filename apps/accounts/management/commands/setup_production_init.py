from decimal import Decimal
import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.accounts.models import CustomUser
from apps.accounts.services import setup_roles_and_permissions, create_institutional_user
from apps.courses.models import AcademicYear, InstitutionSetting
from apps.courses.services import ensure_standard_colegio_grades
from apps.periods.models import AcademicPeriod
import os

class Command(BaseCommand):
    help = 'Inicializa automáticamente usuarios de producción (Admin/Rector), Año Lectivo y Periodos'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('==> [1/4] Configurando grupos y permisos de roles...'))
        setup_roles_and_permissions()

        admin_password = os.getenv('ADMIN_INITIAL_PASSWORD', 'Academix2026!')

        # 1. Superadministrador
        if not CustomUser.objects.filter(username='admin').exists():
            create_institutional_user(
                username='admin',
                email='admin@academix.edu.co',
                password=admin_password,
                role=CustomUser.Role.ADMIN,
                document_type=CustomUser.DocumentType.CC,
                document_number='1000000001',
                first_name='Administrador',
                last_name='General',
                phone='3001234567',
                address='Sede Central ACADEMIX',
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(self.style.SUCCESS(f'    [OK] Superusuario creado: admin / {admin_password}'))
        else:
            self.stdout.write(self.style.NOTICE('    [INFO] Usuario admin ya existe.'))

        # 2. Rector
        if not CustomUser.objects.filter(username='rector').exists():
            create_institutional_user(
                username='rector',
                email='rector@academix.edu.co',
                password=admin_password,
                role=CustomUser.Role.RECTOR,
                document_type=CustomUser.DocumentType.CC,
                document_number='1000000002',
                first_name='Rector',
                last_name='Institucional',
                phone='3007654321',
                address='Despacho de Rectoría ACADEMIX',
                is_staff=True,
                is_superuser=False
            )
            self.stdout.write(self.style.SUCCESS(f'    [OK] Usuario Rector creado: rector / {admin_password}'))
        else:
            self.stdout.write(self.style.NOTICE('    [INFO] Usuario rector ya existe.'))

        # 3. Parametrización Institucional
        self.stdout.write(self.style.NOTICE('==> [2/4] Verificando parametrización institucional...'))
        inst_setting = InstitutionSetting.get_settings()
        if not inst_setting.institution_name or inst_setting.institution_name == 'Institución Educativa':
            inst_setting.institution_name = 'ACADEMIX'
            inst_setting.save()
        ensure_standard_colegio_grades(scope=inst_setting.school_scope)
        self.stdout.write(self.style.SUCCESS('    [OK] Grados escolares de Transición a 11° verificados.'))

        # 4. Año Lectivo
        self.stdout.write(self.style.NOTICE('==> [3/4] Verificando Año Lectivo vigente...'))
        current_year = AcademicYear.objects.filter(is_current=True).first()
        if not current_year:
            current_year = AcademicYear.objects.create(
                year=2026,
                name='Año Escolar 2026-2027',
                start_date=datetime.date(2026, 1, 15),
                end_date=datetime.date(2026, 11, 30),
                is_current=True,
                status=AcademicYear.Status.ACTIVE
            )
            self.stdout.write(self.style.SUCCESS('    [OK] Año Lectivo 2026-2027 creado y activado.'))
        else:
            self.stdout.write(self.style.NOTICE(f'    [INFO] Año Lectivo activo: {current_year.name}'))

        # 5. Periodos Académicos
        self.stdout.write(self.style.NOTICE('==> [4/4] Verificando Periodos Académicos...'))
        if not AcademicPeriod.objects.filter(academic_year=current_year).exists():
            periods_def = [
                (1, 'Periodo 1 (Primer Bimestre)', datetime.date(2026, 1, 15), datetime.date(2026, 4, 10), AcademicPeriod.Status.ACTIVE),
                (2, 'Periodo 2 (Segundo Bimestre)', datetime.date(2026, 4, 11), datetime.date(2026, 6, 20), AcademicPeriod.Status.ACTIVE),
                (3, 'Periodo 3 (Tercer Bimestre)', datetime.date(2026, 7, 10), datetime.date(2026, 9, 15), AcademicPeriod.Status.ACTIVE),
                (4, 'Periodo 4 (Cuarto Bimestre)', datetime.date(2026, 9, 16), datetime.date(2026, 11, 28), AcademicPeriod.Status.ACTIVE),
            ]
            for num, name, start, end, status in periods_def:
                AcademicPeriod.objects.create(
                    academic_year=current_year,
                    number=num,
                    name=name,
                    start_date=start,
                    end_date=end,
                    percentage=Decimal('25.00'),
                    status=status
                )
            self.stdout.write(self.style.SUCCESS('    [OK] 4 Periodos académicos creados exitosamente.'))
        else:
            self.stdout.write(self.style.NOTICE('    [INFO] Periodos académicos ya configurados.'))

        self.stdout.write(self.style.SUCCESS('\n*** INICIALIZACION DE PRODUCCION COMPLETADA CON EXITO ***\n'))
