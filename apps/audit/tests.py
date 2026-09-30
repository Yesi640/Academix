from django.test import TestCase, RequestFactory
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import HttpResponse
from apps.accounts.models import CustomUser
from apps.accounts.services import create_institutional_user
from apps.audit.models import AuditLog, AuditTrail
from apps.audit.services import (
    log_audit,
    audit_grade_change,
    audit_observation_deletion,
    audit_official_export,
    calculate_dict_diff,
)
from apps.audit.selectors import (
    get_audit_trail_for_entity,
    get_critical_audit_logs,
    get_audit_trail_for_user,
)
from apps.audit.decorators import audit_action


class AuditLogTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = create_institutional_user(
            username='auditor_test',
            email='auditor@academix.edu.co',
            password='Password123*',
            role=CustomUser.Role.ADMIN
        )

    def test_log_creation_and_values(self):
        request = self.factory.get('/dashboard/')
        request.user = self.user

        log = log_audit(
            action=AuditLog.Action.UPDATE,
            table_name='GradeRecord',
            record_id=101,
            old_values={'score': '3.50'},
            new_values={'score': '4.20'},
            reason='Corrección justificada de nota',
            user=self.user,
            request=request
        )

        self.assertIsNotNone(log.id)
        self.assertEqual(log.action, AuditLog.Action.UPDATE)
        self.assertEqual(log.table_name, 'GradeRecord')
        self.assertEqual(log.old_values.get('score'), '3.50')
        self.assertEqual(log.new_values.get('score'), '4.20')
        self.assertEqual(log.user, self.user)
        self.assertEqual(AuditTrail, AuditLog)

    def test_immutability_on_update(self):
        log = log_audit(
            action=AuditLog.Action.INSERT,
            table_name='CustomUser',
            record_id=1,
            reason='Creación de usuario',
            user=self.user
        )
        log.reason = 'Modificación no autorizada'
        with self.assertRaises(PermissionDenied):
            log.save()

    def test_immutability_on_delete(self):
        log = log_audit(
            action=AuditLog.Action.INSERT,
            table_name='CustomUser',
            record_id=1,
            reason='Creación de usuario',
            user=self.user
        )
        with self.assertRaises(PermissionDenied):
            log.delete()

    def test_immutability_on_bulk_queryset(self):
        log_audit(
            action=AuditLog.Action.LOGIN,
            table_name='CustomUser',
            record_id=self.user.id,
            reason='Login normal',
            user=self.user
        )
        with self.assertRaises(PermissionDenied):
            AuditLog.objects.filter(table_name='CustomUser').delete()

        with self.assertRaises(PermissionDenied):
            AuditLog.objects.filter(table_name='CustomUser').update(reason='Hack')

    def test_audit_grade_change_service(self):
        log = audit_grade_change(
            grade_record_id=55,
            old_score='2.50',
            new_score='4.00',
            student_name='Pepito Pérez',
            subject_code='MAT-01',
            criterion_name='Examen Final',
            reason='Recalificación por error de transcripción',
            user=self.user
        )
        self.assertEqual(log.action, AuditLog.Action.GRADE_OVERRIDE)
        self.assertEqual(log.table_name, 'GradeRecord')
        self.assertEqual(log.old_values['score'], '2.50')
        self.assertEqual(log.new_values['score'], '4.00')

    def test_audit_observation_deletion_service(self):
        log = audit_observation_deletion(
            observation_id=12,
            student_name='Juanito Alimaña',
            author_name='Prof. Gómez',
            content_snippet='Falta leve en formación...',
            reason='Revisión de comité de convivencia',
            user=self.user
        )
        self.assertEqual(log.action, AuditLog.Action.OBSERVATION_DELETED)
        self.assertEqual(log.table_name, 'DisciplineRecord')

    def test_audit_selectors(self):
        audit_official_export('SIMAT_ESTUDIANTES', {'year': 2026}, 'simat_2026.csv', user=self.user)
        logs = get_audit_trail_for_entity('OfficialReports')
        self.assertTrue(logs.exists())
        self.assertEqual(logs.first().new_values['filename'], 'simat_2026.csv')

        critical = get_critical_audit_logs()
        self.assertIsNotNone(critical)

    def test_audit_decorator(self):
        @audit_action(action=AuditLog.Action.GRADE_OVERRIDE, table_name='TestGrade', reason_required=True)
        def my_view(request):
            return HttpResponse('OK')

        # Sin justificación -> ValidationError
        req_without_reason = self.factory.post('/grades/edit/', data={})
        req_without_reason.user = self.user
        with self.assertRaises(ValidationError):
            my_view(req_without_reason)

        # Con justificación -> Éxito y registro en auditoría
        req_with_reason = self.factory.post('/grades/edit/', data={'reason': 'Aprobada por rectoría'})
        req_with_reason.user = self.user
        resp = my_view(req_with_reason)
        self.assertEqual(resp.status_code, 200)

        last_log = AuditLog.objects.first()
        self.assertEqual(last_log.action, AuditLog.Action.GRADE_OVERRIDE)
        self.assertEqual(last_log.reason, 'Aprobada por rectoría')
