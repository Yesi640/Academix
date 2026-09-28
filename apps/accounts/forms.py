import random
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import CustomUser
from apps.students.models import StudentProfile
from apps.courses.models import CourseSection

LOGIN_ROLES = [
    ('RECTOR', 'Rector / Rectora'),
    ('TEACHER', 'Docente'),
    ('STUDENT', 'Alumno'),
    ('PARENT', 'Padre de Familia'),
    ('SECRETARIA', 'Secretaria'),
]

class LoginForm(forms.Form):
    role = forms.ChoiceField(
        choices=LOGIN_ROLES,
        initial='TEACHER',
        widget=forms.Select(attrs={
            'class': 'form-select form-select-sm',
            'id': 'login-role-select',
        }),
        label='Seleccione su Rol'
    )
    username = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Nombre de Usuario o Documento',
            'autocomplete': 'username',
            'id': 'login-username-input',
        }),
        label='Usuario o Identificación'
    )
    student_id = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm font-monospace fw-bold text-primary',
            'placeholder': 'Ej: ALU-2026-1001 o Código',
            'id': 'login-student-id-input',
        }),
        label='ID ÚNICO del Alumno (Obligatorio)'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Contraseña',
            'autocomplete': 'current-password',
            'id': 'login-password-input',
        }),
        label='Contraseña'
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        username = cleaned_data.get('username', '').strip()
        student_id = cleaned_data.get('student_id', '').strip()
        password = cleaned_data.get('password')

        if not password:
            raise ValidationError("Debe ingresar su contraseña.")

        # 1. Validación para ALUMNO
        if role == 'STUDENT':
            ident = (student_id or username).strip()
            if not ident:
                raise ValidationError("Debe ingresar su ID ÚNICO, Usuario institucional o Documento para iniciar sesión.")

            # Buscar perfil de estudiante por su ID ÚNICO, documento, username o correo
            student_profile = (
                StudentProfile.objects.filter(student_code__iexact=ident).select_related('user').first()
                or StudentProfile.objects.filter(user__document_number=ident).select_related('user').first()
                or StudentProfile.objects.filter(user__username__iexact=ident).select_related('user').first()
                or StudentProfile.objects.filter(user__email__iexact=ident).select_related('user').first()
            )

            if not student_profile:
                raise ValidationError(f"No se encontró ningún alumno con la identificación '{ident}'. Verifique su ID ÚNICO, documento o usuario.")

            user = authenticate(self.request, username=student_profile.user.username, password=password)
            if not user:
                raise ValidationError("Contraseña incorrecta para el alumno.")

            if user.role != CustomUser.Role.STUDENT:
                raise ValidationError("El usuario no corresponde al rol de Alumno seleccionado.")

            self.user_cache = user

        # 2. Validación para PADRE DE FAMILIA
        elif role == 'PARENT':
            from apps.courses.models import InstitutionSetting
            institution = InstitutionSetting.get_settings()
            if not institution.has_parents:
                raise ValidationError("El rol de Acudiente / Padre de Familia solo está habilitado para el modelo de Colegio.")

            if not student_id:
                raise ValidationError("El ID ÚNICO del alumno es obligatorio para el acceso del padre de familia.")
            if not username:
                raise ValidationError("Debe ingresar el usuario o documento del padre de familia.")

            student_profile = StudentProfile.objects.filter(student_code__iexact=student_id).first()
            if not student_profile:
                student_profile = StudentProfile.objects.filter(user__document_number=student_id).first()

            if not student_profile:
                raise ValidationError(f"No existe ningún alumno registrado con el ID ÚNICO '{student_id}'.")

            user = authenticate(self.request, username=username, password=password)
            if not user:
                raise ValidationError("Credenciales inválidas para el Padre de Familia.")

            if user.role != CustomUser.Role.PARENT:
                raise ValidationError("El usuario no corresponde al rol de Padre de Familia seleccionado.")

            # Verificar vinculación de parentesco estricta
            user_children = StudentProfile.objects.filter(parent=user)
            if user_children.exists():
                if not user_children.filter(id=student_profile.id).exists():
                    raise ValidationError("El ID ÚNICO ingresado no coincide con los alumnos asociados a su cuenta de acudiente.")
            else:
                if student_profile.parent and student_profile.parent_id != user.id:
                    raise ValidationError("El ID ÚNICO ingresado ya se encuentra registrado con otro acudiente.")
                else:
                    student_profile.parent = user
                    student_profile.save()

            self.user_cache = user

        # 3. Validación para PROFESOR o SECRETARIA
        else:
            if not username:
                raise ValidationError("Debe ingresar su usuario o documento institucional.")

            user = authenticate(self.request, username=username, password=password)
            if not user:
                raise ValidationError("Credenciales inválidas. Verifique su usuario y contraseña.")

            # Verificar coincidencia estricta de rol
            if role == 'TEACHER' and not (user.is_teacher or user.is_admin_role):
                raise ValidationError("El usuario no corresponde al rol de Docente seleccionado.")
            elif role == 'SECRETARIA' and not (user.is_secretary or user.is_admin_role or user.is_rector):
                raise ValidationError("El usuario no corresponde al rol de Secretaría seleccionado.")

            self.user_cache = user

        return cleaned_data

    def get_user(self):
        return self.user_cache


class RegistrationForm(forms.Form):
    role = forms.ChoiceField(
        choices=LOGIN_ROLES,
        initial='STUDENT',
        widget=forms.Select(attrs={'class': 'form-select form-select-sm border-primary', 'id': 'reg-role-select'}),
        label='Seleccione el Rol a Registrar'
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Elija un nombre de usuario'}),
        label='Nombre de Usuario'
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'}),
        label='Nombres'
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
        label='Apellidos'
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.edu'}),
        label='Correo Electrónico (Opcional)'
    )
    document_type = forms.ChoiceField(
        choices=CustomUser.DocumentType.choices,
        initial=CustomUser.DocumentType.TI,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Tipo de Documento'
    )
    document_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de documento de identidad'}),
        label='Número de Documento'
    )
    student_id_target = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control font-monospace fw-bold text-primary',
            'placeholder': 'Ej: ALU-2026-1001',
            'id': 'reg-student-id-input'
        }),
        label='ID ÚNICO del Alumno Representado (Solo Padres)'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña segura'}),
        label='Contraseña'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repita la contraseña'}),
        label='Confirmar Contraseña'
    )

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip().lower()
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("Este nombre de usuario ya está registrado.")
        return username

    def clean_document_number(self):
        doc = self.cleaned_data.get('document_number', '').strip()
        if CustomUser.objects.filter(document_number=doc).exists():
            raise ValidationError("Ya existe un usuario con este número de documento.")
        return doc

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        role = cleaned_data.get('role')
        student_id_target = cleaned_data.get('student_id_target', '').strip()

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Las contraseñas no coinciden.")

        if role == 'PARENT':
            from apps.courses.models import InstitutionSetting
            institution = InstitutionSetting.get_settings()
            if not institution.has_parents:
                raise ValidationError("El registro de Acudientes / Padres de Familia solo está habilitado para el modelo de Colegio.")

            if not student_id_target:
                raise ValidationError("Para registrarse como Padre de Familia, es OBLIGATORIO ingresar el ID ÚNICO del alumno.")
            student_profile = StudentProfile.objects.filter(student_code__iexact=student_id_target).first()
            if not student_profile:
                student_profile = StudentProfile.objects.filter(user__document_number=student_id_target).first()
            if not student_profile:
                raise ValidationError(f"No existe ningún alumno en el sistema con el ID ÚNICO '{student_id_target}'.")
            cleaned_data['target_student_profile'] = student_profile

        return cleaned_data


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }
