from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
import re
from .models import Usuario, Asistencia, RegistroFalla, RegistroLlamada


def validar_rut_chileno_form(rut):
    """Valida el formato de RUT chileno para formularios"""
    if not rut:
        return
    
    # Limpiar espacios y convertir a mayúsculas
    rut = rut.strip().upper()
    
    # Patrón: 12345678-0 o 1234567-8 (8 o 7 dígitos, guion, dígito verificador 0-9 o K)
    patron = r'^\d{7,8}-[0-9K]$'
    if not re.match(patron, rut):
        raise ValidationError('El RUT debe tener el formato 12345678-0 o 1234567-8 (dígito verificador: 0-9 o K)')
    
    # Validar dígito verificador
    rut_parts = rut.split('-')
    numero = rut_parts[0]
    dv = rut_parts[1]
    
    # Calcular dígito verificador
    suma = 0
    multiplicador = 2
    
    for digito in reversed(numero):
        suma += int(digito) * multiplicador
        multiplicador += 1
        if multiplicador > 7:
            multiplicador = 2
    
    resto = suma % 11
    dv_calculado = 11 - resto
    
    if dv_calculado == 11:
        dv_calculado = '0'
    elif dv_calculado == 10:
        dv_calculado = 'K'
    else:
        dv_calculado = str(dv_calculado)
    
    if dv != dv_calculado:
        raise ValidationError('El dígito verificador del RUT es incorrecto')


class CrearUsuarioForm(forms.ModelForm):
    """Formulario para crear usuarios desde el panel de administrador"""
    nombre = forms.CharField(
        min_length=4,
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre (mínimo 4 caracteres)',
            'maxlength': '20',
            'minlength': '4'
        }),
        error_messages={
            'required': 'El nombre es obligatorio',
            'min_length': 'El nombre debe tener al menos 4 caracteres',
            'max_length': 'El nombre no puede exceder 20 caracteres'
        }
    )
    
    apellido = forms.CharField(
        min_length=4,
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apellido (mínimo 4 caracteres)',
            'maxlength': '20',
            'minlength': '4'
        }),
        error_messages={
            'required': 'El apellido es obligatorio',
            'min_length': 'El apellido debe tener al menos 4 caracteres',
            'max_length': 'El apellido no puede exceder 20 caracteres'
        }
    )
    
    rut = forms.CharField(
        max_length=12,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678-0',
            'maxlength': '12'
        }),
        validators=[validar_rut_chileno_form],
        error_messages={
            'required': 'El RUT es obligatorio'
        }
    )
    
    correo_institucional = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@institucional.cl',
            'type': 'email'
        }),
        error_messages={
            'required': 'El correo institucional es obligatorio',
            'invalid': 'Ingrese un correo electrónico válido'
        }
    )
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            nombre = nombre.strip()
            if len(nombre) < 4:
                raise ValidationError('El nombre debe tener al menos 4 caracteres')
        return nombre
    
    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido')
        if apellido:
            apellido = apellido.strip()
            if len(apellido) < 4:
                raise ValidationError('El apellido debe tener al menos 4 caracteres')
        return apellido
    
    
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'rut', 'correo_institucional']
    
    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if rut:
            rut = rut.strip().upper()
            # Verificar si el RUT ya existe
            if Usuario.objects.filter(rut=rut).exists():
                raise ValidationError('Este RUT ya está registrado en el sistema')
        return rut
    
    def clean_correo_institucional(self):
        correo = self.cleaned_data.get('correo_institucional')
        if correo:
            # Verificar si el correo ya existe
            if Usuario.objects.filter(correo_institucional=correo).exists():
                raise ValidationError('Este correo institucional ya está registrado')
        return correo
    
    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre', '').strip()
        apellido = cleaned_data.get('apellido', '').strip()
        
        # Verificar que el username generado no exista
        if nombre and apellido:
            # Generar username: primera letra del nombre + apellido completo (sin espacios, en minúsculas)
            username_base = (nombre[0] + apellido.replace(' ', '')).lower()
            username_final = username_base
            
            # Si el username ya existe, agregar números
            counter = 1
            while Usuario.objects.filter(username=username_final).exists():
                username_final = f"{username_base}{counter}"
                counter += 1
            
            cleaned_data['username_generated'] = username_final
        
        return cleaned_data
    
    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.rol = 'usuario'  # Los usuarios creados son siempre 'usuario'
        usuario.email = self.cleaned_data['correo_institucional']
        
        # Generar username: primera letra del nombre + apellido completo (sin espacios, en minúsculas)
        nombre = self.cleaned_data['nombre'].strip()
        apellido = self.cleaned_data['apellido'].strip().replace(' ', '')
        username_base = (nombre[0] + apellido).lower()
        username_final = username_base
        
        # Si el username ya existe, agregar números
        counter = 1
        while Usuario.objects.filter(username=username_final).exists():
            username_final = f"{username_base}{counter}"
            counter += 1
        
        usuario.username = username_final
        
        # Contraseña por defecto: "popup"
        usuario.set_password('popup')
        usuario.cambio_password_requerido = True  # Requerir cambio de contraseña en primer login
        
        if commit:
            usuario.save()
        return usuario


class EditarUsuarioForm(forms.ModelForm):
    """Formulario para editar usuarios desde el panel de administrador"""
    nombre = forms.CharField(
        min_length=4,
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre (mínimo 4 caracteres)',
            'maxlength': '20',
            'minlength': '4'
        }),
        error_messages={
            'required': 'El nombre es obligatorio',
            'min_length': 'El nombre debe tener al menos 4 caracteres',
            'max_length': 'El nombre no puede exceder 20 caracteres'
        }
    )
    
    apellido = forms.CharField(
        min_length=4,
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apellido (mínimo 4 caracteres)',
            'maxlength': '20',
            'minlength': '4'
        }),
        error_messages={
            'required': 'El apellido es obligatorio',
            'min_length': 'El apellido debe tener al menos 4 caracteres',
            'max_length': 'El apellido no puede exceder 20 caracteres'
        }
    )
    
    rut = forms.CharField(
        max_length=12,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678-0',
            'maxlength': '12'
        }),
        validators=[validar_rut_chileno_form],
        error_messages={
            'required': 'El RUT es obligatorio'
        }
    )
    
    correo_institucional = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@institucional.cl',
            'type': 'email'
        }),
        error_messages={
            'required': 'El correo institucional es obligatorio',
            'invalid': 'Ingrese un correo electrónico válido'
        }
    )
    
    rol = forms.ChoiceField(
        choices=Usuario.ROL_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Rol'
    )
    
    activo = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Usuario Activo'
    )
    
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'rut', 'correo_institucional', 'rol', 'activo']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Si es edición, cargar los datos existentes
            self.fields['nombre'].initial = self.instance.nombre
            self.fields['apellido'].initial = self.instance.apellido
            self.fields['rut'].initial = self.instance.rut
            self.fields['correo_institucional'].initial = self.instance.correo_institucional
            self.fields['rol'].initial = self.instance.rol
            self.fields['activo'].initial = self.instance.activo
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            nombre = nombre.strip()
            if len(nombre) < 4:
                raise ValidationError('El nombre debe tener al menos 4 caracteres')
        return nombre
    
    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido')
        if apellido:
            apellido = apellido.strip()
            if len(apellido) < 4:
                raise ValidationError('El apellido debe tener al menos 4 caracteres')
        return apellido
    
    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if rut:
            rut = rut.strip().upper()
            # Verificar si el RUT ya existe (excepto para el usuario actual)
            existing_usuario = Usuario.objects.filter(rut=rut).exclude(pk=self.instance.pk if self.instance.pk else None).first()
            if existing_usuario:
                raise ValidationError('Este RUT ya está registrado en el sistema')
        return rut
    
    def clean_correo_institucional(self):
        correo = self.cleaned_data.get('correo_institucional')
        if correo:
            # Verificar si el correo ya existe (excepto para el usuario actual)
            existing_usuario = Usuario.objects.filter(correo_institucional=correo).exclude(pk=self.instance.pk if self.instance.pk else None).first()
            if existing_usuario:
                raise ValidationError('Este correo institucional ya está registrado')
        return correo
    
    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.email = self.cleaned_data['correo_institucional']
        
        if commit:
            usuario.save()
        return usuario


class CambiarPasswordForm(forms.Form):
    """Formulario para cambiar la contraseña en el primer login"""
    password_actual = forms.CharField(
        label='Contraseña Actual',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña actual'
        }),
        required=True,
        error_messages={
            'required': 'La contraseña actual es obligatoria'
        }
    )
    
    password_nueva = forms.CharField(
        label='Nueva Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su nueva contraseña'
        }),
        required=True,
        min_length=8,
        error_messages={
            'required': 'La nueva contraseña es obligatoria',
            'min_length': 'La contraseña debe tener al menos 8 caracteres'
        }
    )
    
    password_confirmacion = forms.CharField(
        label='Confirmar Nueva Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme su nueva contraseña'
        }),
        required=True,
        error_messages={
            'required': 'La confirmación de contraseña es obligatoria'
        }
    )
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_password_actual(self):
        password_actual = self.cleaned_data.get('password_actual')
        if not self.user.check_password(password_actual):
            raise ValidationError('La contraseña actual es incorrecta')
        return password_actual
    
    def clean_password_confirmacion(self):
        password_nueva = self.cleaned_data.get('password_nueva')
        password_confirmacion = self.cleaned_data.get('password_confirmacion')
        
        if password_nueva and password_confirmacion:
            if password_nueva != password_confirmacion:
                raise ValidationError('Las contraseñas no coinciden')
        
        return password_confirmacion
    
    def clean_password_nueva(self):
        password_nueva = self.cleaned_data.get('password_nueva')
        password_actual = self.cleaned_data.get('password_actual')
        
        if password_nueva and password_actual:
            if password_nueva == password_actual:
                raise ValidationError('La nueva contraseña debe ser diferente a la contraseña actual')
        
        # Validar la contraseña con los validadores de Django
        try:
            validate_password(password_nueva, self.user)
        except ValidationError as e:
            raise ValidationError(e.messages)
        
        return password_nueva
    
    def save(self):
        password_nueva = self.cleaned_data['password_nueva']
        self.user.set_password(password_nueva)
        self.user.cambio_password_requerido = False
        self.user.save()
        return self.user


class RegistroAsistenciaForm(forms.Form):
    """Formulario para registro de asistencia por turno"""
    TURNO_CHOICES = [
        ('apertura', 'Apertura (09:00 - 13:00)'),
        ('tarde', 'Tarde (13:00 - 17:00)'),
        ('cierre', 'Cierre (17:00 - 21:00)'),
    ]
    
    turno = forms.ChoiceField(
        choices=TURNO_CHOICES,
        required=True,
        widget=forms.RadioSelect(attrs={
            'class': 'turno-radio'
        }),
        label='Selecciona tu turno',
        error_messages={
            'required': 'Debes seleccionar un turno'
        }
    )


class EditarAsistenciaForm(forms.ModelForm):
    """Formulario para editar asistencia"""
    TURNO_CHOICES = [
        ('apertura', 'Apertura (09:00 - 13:00)'),
        ('tarde', 'Tarde (13:00 - 17:00)'),
        ('cierre', 'Cierre (17:00 - 21:00)'),
    ]
    
    turno = forms.ChoiceField(
        choices=TURNO_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Turno'
    )
    
    class Meta:
        model = Asistencia
        fields = ['turno', 'fecha']
        widgets = {
            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }
        labels = {
            'fecha': 'Fecha'
        }
    
    def save(self, commit=True):
        asistencia = super().save(commit=False)
        turno = self.cleaned_data['turno']
        
        # Mapear turno a horas de entrada y salida (horario chileno GMT-3)
        horarios_turno = {
            'apertura': {'entrada': '09:00', 'salida': '13:00'},
            'tarde': {'entrada': '13:00', 'salida': '17:00'},
            'cierre': {'entrada': '17:00', 'salida': '21:00'}
        }
        horario = horarios_turno.get(turno, {'entrada': '09:00', 'salida': '13:00'})
        from datetime import datetime
        asistencia.hora_entrada = datetime.strptime(horario['entrada'], '%H:%M').time()
        asistencia.hora_salida = datetime.strptime(horario['salida'], '%H:%M').time()
        
        if commit:
            asistencia.save()
        return asistencia


class RegistroFallaForm(forms.ModelForm):
    """Formulario para registrar fallas en las máquinas"""
    
    class Meta:
        model = RegistroFalla
        fields = ['maquina', 'descripcion', 'observaciones', 'fecha']
        widgets = {
            'maquina': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código de la máquina'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe la falla en detalle'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones adicionales (opcional)'
            }),
            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }
        labels = {
            'maquina': 'Código de Máquina',
            'descripcion': 'Descripción de la Falla',
            'observaciones': 'Observaciones',
            'fecha': 'Fecha'
        }


class RegistroLlamadaForm(forms.ModelForm):
    """Formulario para registrar llamadas al técnico"""
    
    class Meta:
        model = RegistroLlamada
        fields = ['motivo', 'tecnico_contactado', 'descripcion', 'observaciones', 'fecha']
        widgets = {
            'motivo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Motivo de la llamada'
            }),
            'tecnico_contactado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del técnico contactado'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe el motivo de la llamada en detalle'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones adicionales (opcional)'
            }),
            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }
        labels = {
            'motivo': 'Motivo de la Llamada',
            'tecnico_contactado': 'Técnico Contactado',
            'descripcion': 'Descripción',
            'observaciones': 'Observaciones',
            'fecha': 'Fecha'
        }
