from django.test import TestCase, Client
from django.urls import reverse
from apps.accounts.models import CustomUser
from apps.accounts.services import create_institutional_user, setup_roles_and_permissions

class AccountsModelTests(TestCase):
    def setUp(self):
        setup_roles_and_permissions()
        self.user = create_institutional_user(
            username='profesor1',
            email='profesor1@academix.edu.co',
            password='SecurePassword123!',
            role=CustomUser.Role.TEACHER,
            document_type=CustomUser.DocumentType.CC,
            document_number='987654321',
            first_name='Juan',
            last_name='Pérez'
        )

    def test_user_creation_and_role_properties(self):
        self.assertEqual(self.user.role, CustomUser.Role.TEACHER)
        self.assertTrue(self.user.is_teacher)
        self.assertFalse(self.user.is_admin_role)
        self.assertEqual(self.user.get_role_display(), 'Docente')
        self.assertEqual(self.user.groups.count(), 1)
        self.assertEqual(self.user.groups.first().name, 'Docentes')

    def test_login_flow(self):
        client = Client()
        response = client.post(reverse('accounts:login'), {
            'username': 'profesor1',
            'password': 'SecurePassword123!',
            'role': CustomUser.Role.TEACHER
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/dashboard/', response.url)

    def test_admin_role_properties(self):
        admin_user = create_institutional_user(
            username='admin_test',
            email='admin@academix.edu.co',
            password='AdminPassword123!',
            role=CustomUser.Role.ADMIN,
            is_staff=True,
            is_superuser=True
        )
        self.assertTrue(admin_user.is_admin_role)
        self.assertTrue(admin_user.is_staff)

    def test_switch_institution_model_endpoint(self):
        from apps.courses.models import InstitutionSetting
        client = Client()
        response = client.get(reverse('accounts:switch_model') + '?model=SENA_TECNICO')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['model'], 'SENA_TECNICO')
        self.assertEqual(data['terms']['student'], 'Aprendiz')

        settings = InstitutionSetting.get_settings()
        self.assertEqual(settings.institution_type, 'SENA_TECNICO')
        self.assertEqual(settings.term_student, 'Aprendiz')

    def test_register_view_with_model_param(self):
        client = Client()
        response = client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Registro en ACADEMIX')

