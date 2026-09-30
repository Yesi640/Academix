from django.core.exceptions import PermissionDenied
from .services import (
    get_institution_settings,
    is_public_school_mode,
    is_private_school_mode,
    is_feature_active,
    can_download_report_card,
)


class PublicSchoolOnlyMixin:
    """
    Mixin para CBVs que restringe la vista exclusivamente a Colegios Públicos / Oficiales.
    Lanza PermissionDenied si el colegio opera en modo privado.
    """
    def dispatch(self, request, *args, **kwargs):
        if not is_public_school_mode():
            raise PermissionDenied(
                "Esta vista está reservada exclusivamente para instituciones educativas públicas/oficiales."
            )
        return super().dispatch(request, *args, **kwargs)


class PrivateSchoolOnlyMixin:
    """
    Mixin para CBVs que restringe la vista exclusivamente a Colegios Privados.
    Lanza PermissionDenied si el colegio opera en modo oficial.
    """
    def dispatch(self, request, *args, **kwargs):
        if not is_private_school_mode():
            raise PermissionDenied(
                "Esta vista está reservada exclusivamente para instituciones educativas privadas."
            )
        return super().dispatch(request, *args, **kwargs)


class InstitutionFeatureRequiredMixin:
    """
    Mixin para CBVs que exige la activación de una bandera institucional específica.
    Uso:
        class PAEDailyRationView(InstitutionFeatureRequiredMixin, TemplateView):
            required_feature = 'enable_pae_module'
    """
    required_feature = None

    def dispatch(self, request, *args, **kwargs):
        if self.required_feature and not is_feature_active(self.required_feature):
            raise PermissionDenied(
                f"El módulo '{self.required_feature}' no está habilitado en la parametrización de esta institución."
            )
        return super().dispatch(request, *args, **kwargs)


class ReportCardClearanceMixin:
    """
    Mixin para CBVs de descarga o visualización de boletines escolares.
    Aplica la regla de negocio híbrida de gratuidad vs retención por mora.
    """
    student_lookup_field = 'pk'

    def get_student_profile(self, request, *args, **kwargs):
        from apps.students.models import StudentProfile
        student_id = kwargs.get(self.student_lookup_field) or request.GET.get('student_id')
        if student_id:
            return StudentProfile.objects.filter(id=student_id).first()
        if hasattr(request.user, 'student_profile'):
            return request.user.student_profile
        return None

    def dispatch(self, request, *args, **kwargs):
        student = self.get_student_profile(request, *args, **kwargs)
        if student:
            can_download, reason = can_download_report_card(student)
            if not can_download:
                raise PermissionDenied(f"Acceso al boletín restringido: {reason}")
        return super().dispatch(request, *args, **kwargs)
