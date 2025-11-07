from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from PIL import Image
import re
import os
from .models import Usuario, Asistencia, RegistroFalla, RegistroLlamada, Inventario, Pedido, ImagenCarrusel, Evento, Noticia, Contacto, ManualInterno


def validar_rut_chileno_form(rut):
    """Valida el formato de RUT chileno para formularios (solo formato, no dígito verificador matemático)"""
    if not rut:
        return
    
    # Limpiar espacios y convertir a mayúsculas
    rut = rut.strip().upper()
    
    # Remover puntos si existen (formato chileno común: 12.345.678-0)
    rut = rut.replace('.', '')
    
    # Patrón: 12345678-0 o 1234567-8 (7 u 8 dígitos, guion, dígito verificador 0-9 o K)
    patron = r'^\d{7,8}-[0-9K]$'
    if not re.match(patron, rut):
        raise ValidationError('El RUT debe tener el formato 12345678-0 o 1234567-8 (dígito verificador: 0-9 o K)')
    
    # Validar que tenga el formato correcto
    rut_parts = rut.split('-')
    if len(rut_parts) != 2:
        raise ValidationError('El RUT debe tener el formato 12345678-0 o 1234567-8')
    
    numero = rut_parts[0]
    dv = rut_parts[1]
    
    # Verificar que el número tenga entre 7 y 8 dígitos
    if len(numero) < 7 or len(numero) > 8:
        raise ValidationError('El RUT debe tener entre 7 y 8 dígitos antes del guion')
    
    # Verificar que el dígito verificador sea un número (0-9) o K
    if dv not in '0123456789K':
        raise ValidationError('El dígito verificador debe ser un número del 0 al 9 o la letra K')
    
    # No se valida el dígito verificador matemáticamente, solo el formato


def validar_imagen_evento_noticia(imagen):
    """Valida el tamaño, formato y dimensiones de las imágenes para eventos y noticias"""
    # Si no hay imagen (None o archivo vacío), no validar (permitir campos vacíos)
    if not imagen or imagen == '':
        return
    
    # Validar tamaño de archivo (5MB máximo)
    max_size = 5 * 1024 * 1024  # 5MB en bytes
    if imagen.size > max_size:
        raise ValidationError(f'El tamaño de la imagen no puede exceder 5MB. Tamaño actual: {imagen.size / (1024*1024):.2f}MB')
    
    # Validar formato de archivo
    extensiones_permitidas = ['.jpg', '.jpeg', '.png']
    nombre_archivo = imagen.name.lower()
    extension = os.path.splitext(nombre_archivo)[1]
    
    if extension not in extensiones_permitidas:
        raise ValidationError(f'Formato no permitido. Use: JPG, JPEG o PNG. Formato actual: {extension}')
    
    # Validar que sea una imagen válida usando PIL
    try:
        img = Image.open(imagen)
        img.verify()
        
        # Reiniciar el archivo después de verificar
        imagen.seek(0)
        img = Image.open(imagen)
        
        # Validar dimensiones (opcional pero recomendado)
        width, height = img.size
        
        # Verificar proporción recomendada (3:2 o 16:9)
        ratio = width / height if height > 0 else 0
        ratio_3_2 = 1.5  # 3:2
        ratio_16_9 = 16/9  # aproximadamente 1.78
        
        # Advertencia si la proporción no es ideal (pero no bloquea)
        if ratio < 1.2 or ratio > 2.5:
            # No bloqueamos, solo informamos que la proporción no es ideal
            pass
        
        # Validar dimensiones mínimas
        if width < 400 or height < 200:
            raise ValidationError(f'Las dimensiones mínimas recomendadas son 400x200 píxeles. Dimensiones actuales: {width}x{height} píxeles')
        
        # Validar dimensiones máximas razonables
        if width > 5000 or height > 5000:
            raise ValidationError(f'Las dimensiones son demasiado grandes. Máximo recomendado: 5000x5000 píxeles. Dimensiones actuales: {width}x{height} píxeles')
        
    except Exception as e:
        if isinstance(e, ValidationError):
            raise e
        raise ValidationError('El archivo no es una imagen válida o está corrupto.')


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
    
    es_administrador = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Es Administrador',
        help_text='Marcar si el usuario es Administrador'
    )
    
    es_empleado = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Es Empleado',
        help_text='Marcar si el usuario es Empleado'
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
        fields = ['nombre', 'apellido', 'rut', 'correo_institucional', 'es_administrador', 'es_empleado']
    
    def clean(self):
        cleaned_data = super().clean()
        es_administrador = cleaned_data.get('es_administrador', False)
        es_empleado = cleaned_data.get('es_empleado', False)
        
        # Validar que el usuario tenga al menos un rol
        if not es_administrador and not es_empleado:
            raise ValidationError('El usuario debe tener al menos un rol asignado (Administrador o Empleado).')
        
        return cleaned_data
    
    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if rut:
            # Limpiar y normalizar el RUT
            rut = rut.strip().upper().replace('.', '')
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
        # Asignar roles
        usuario._es_administrador = self.cleaned_data.get('es_administrador', False)
        usuario.es_empleado = self.cleaned_data.get('es_empleado', True)
        usuario.email = self.cleaned_data['correo_institucional']
        
        # Todos los usuarios deben cambiar su contraseña en el primer login
        usuario.cambio_password_requerido = True
        
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
    
    es_administrador = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Es Administrador',
        help_text='El usuario tendrá acceso al panel de administración'
    )
    
    es_empleado = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Es Empleado',
        help_text='El usuario podrá registrar asistencia y gestionar stock'
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
        fields = ['nombre', 'apellido', 'rut', 'correo_institucional', 'es_administrador', 'es_empleado', 'activo']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Si es edición, cargar los datos existentes
            self.fields['nombre'].initial = self.instance.nombre
            self.fields['apellido'].initial = self.instance.apellido
            self.fields['rut'].initial = self.instance.rut
            self.fields['correo_institucional'].initial = self.instance.correo_institucional
            # Cargar roles desde los campos booleanos o desde el campo deprecated 'rol'
            if hasattr(self.instance, '_es_administrador'):
                self.fields['es_administrador'].initial = self.instance._es_administrador or (self.instance.rol == 'admin' if self.instance.rol else False)
            else:
                self.fields['es_administrador'].initial = self.instance.rol == 'admin' if self.instance.rol else False
            if hasattr(self.instance, 'es_empleado'):
                self.fields['es_empleado'].initial = self.instance.es_empleado or (self.instance.rol == 'usuario' if self.instance.rol else True)
            else:
                self.fields['es_empleado'].initial = self.instance.rol == 'usuario' if self.instance.rol else True
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
    
    def clean(self):
        cleaned_data = super().clean()
        es_administrador = cleaned_data.get('es_administrador', False)
        es_empleado = cleaned_data.get('es_empleado', False)
        
        # Validar que el usuario tenga al menos un rol
        if not es_administrador and not es_empleado:
            raise ValidationError('El usuario debe tener al menos un rol asignado (Administrador o Empleado).')
        
        return cleaned_data
    
    def save(self, commit=True):
        usuario = super().save(commit=False)
        # Asignar roles desde los campos del formulario
        usuario._es_administrador = self.cleaned_data.get('es_administrador', False)
        usuario.es_empleado = self.cleaned_data.get('es_empleado', False)
        usuario.email = self.cleaned_data['correo_institucional']
        
        # Todos los usuarios deben cambiar su contraseña en el primer login
        # (esto se mantiene desde la creación, no se sobrescribe al editar)
        
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


class CrearInventarioForm(forms.ModelForm):
    """Formulario para crear productos de inventario"""
    
    class Meta:
        model = Inventario
        fields = ['nombre', 'categoria', 'cantidad', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-control'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        labels = {
            'nombre': 'Nombre del Producto',
            'categoria': 'Categoría',
            'cantidad': 'Cantidad',
            'imagen': 'Sube una imagen referencial (máx. 5MB)'
        }
    
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is not None and cantidad < 0:
            raise ValidationError('La cantidad no puede ser negativa')
        return cantidad


class EditarInventarioForm(forms.ModelForm):
    """Formulario para editar productos de inventario"""
    
    class Meta:
        model = Inventario
        fields = ['nombre', 'categoria', 'cantidad', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-control'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        labels = {
            'nombre': 'Nombre del Producto',
            'categoria': 'Categoría',
            'cantidad': 'Cantidad',
            'imagen': 'Sube una imagen referencial (máx. 5MB)'
        }
    
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is not None and cantidad < 0:
            raise ValidationError('La cantidad no puede ser negativa')
        return cantidad


class CambiarStockForm(forms.Form):
    """Formulario simple para que trabajadores cambien solo la cantidad de stock"""
    cantidad = forms.IntegerField(
        label='Nueva Cantidad',
        required=True,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'placeholder': 'Ingrese la nueva cantidad',
            'style': 'text-align: center; font-size: 1.2rem; padding: 15px;'
        }),
        error_messages={
            'required': 'La cantidad es obligatoria',
            'min_value': 'La cantidad no puede ser negativa'
        }
    )


class EditarPrecioProductoForm(forms.ModelForm):
    """Formulario para editar solo el precio de un producto"""
    
    class Meta:
        model = Inventario
        fields = ['precio_unitario']
        widgets = {
            'precio_unitario': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '1',
                'placeholder': '0'
            })
        }
        labels = {
            'precio_unitario': 'Precio Unitario'
        }
    
    def clean_precio_unitario(self):
        precio = self.cleaned_data.get('precio_unitario')
        if precio is not None and precio < 0:
            raise ValidationError('El precio no puede ser negativo')
        # Convertir a entero si tiene decimales
        if precio is not None:
            precio = int(precio)
        return precio


class CrearPedidoForm(forms.ModelForm):
    """Formulario para crear un pedido"""
    
    class Meta:
        model = Pedido
        fields = ['codigo']
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código del pedido'
            })
        }
        labels = {
            'codigo': 'Código del Pedido'
        }


class ImagenCarruselForm(forms.ModelForm):
    """Formulario para gestionar imágenes del carrusel"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Obtener el número máximo de imágenes existentes
        from .models import ImagenCarrusel
        total_imagenes = ImagenCarrusel.objects.filter(activo=True).count()
        
        # Si estamos editando, no contar la imagen actual
        if self.instance and self.instance.pk:
            total_imagenes = ImagenCarrusel.objects.filter(activo=True).exclude(pk=self.instance.pk).count()
        
        # El máximo siempre es 5, pero mostrar información sobre imágenes existentes
        max_orden = min(5, total_imagenes + 1) if total_imagenes < 5 else 5
        
        # Actualizar el campo orden con el máximo disponible
        self.fields['orden'].widget.attrs.update({
            'min': '1',
            'max': '5',
            'maxlength': '1'
        })
        self.fields['orden'].help_text = f'Orden de visualización (1-5). Máximo permitido: 5 imágenes en el carrusel.'
        
        # Si el orden es 1, mostrar placeholder especial
        if self.instance and self.instance.pk and self.instance.orden == 1:
            self.fields['titulo_barista'].widget.attrs['placeholder'] = 'Ej: Barista del Mes - Noviembre 2025'
    
    def clean_orden(self):
        orden = self.cleaned_data.get('orden')
        
        # Validar que el orden esté entre 1 y 5
        if orden is not None:
            if orden < 1:
                raise forms.ValidationError('El orden debe ser mayor o igual a 1.')
            if orden > 5:
                raise forms.ValidationError('El orden no puede ser mayor a 5. Máximo permitido: 5 imágenes en el carrusel.')
            
            # Verificar si ya existe otra imagen con el mismo orden (solo al crear o cambiar orden)
            from .models import ImagenCarrusel
            queryset = ImagenCarrusel.objects.filter(orden=orden, activo=True)
            
            # Si estamos editando, excluir la imagen actual
            if self.instance and self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise forms.ValidationError(f'Ya existe una imagen activa con el orden {orden}. Por favor elija otro orden.')
        
        return orden
    
    def clean(self):
        cleaned_data = super().clean()
        orden = cleaned_data.get('orden')
        titulo_barista = cleaned_data.get('titulo_barista')
        
        # Validar que si orden es 1, se sugiera agregar título del barista
        if orden == 1 and not titulo_barista:
            # No es obligatorio, pero es recomendado
            pass
        
        # Validar que no se exceda el máximo de 5 imágenes activas
        activo = cleaned_data.get('activo', False)
        if activo:
            from .models import ImagenCarrusel
            total_activas = ImagenCarrusel.objects.filter(activo=True).count()
            
            # Si estamos editando y la imagen actual ya estaba activa, no contar esta
            if self.instance and self.instance.pk and self.instance.activo:
                # La imagen ya estaba activa, no incrementamos el contador
                pass
            else:
                # Si estamos creando una nueva imagen activa o activando una inactiva
                total_activas += 1
            
            # Verificar el límite
            if total_activas > 5:
                raise forms.ValidationError({
                    'activo': 'No se pueden tener más de 5 imágenes activas en el carrusel. Por favor desactive otra imagen primero.'
                })
        
        return cleaned_data
    
    class Meta:
        model = ImagenCarrusel
        fields = ['imagen', 'orden', 'titulo_barista', 'activo']
        widgets = {
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'orden': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '5'
            }),
            'titulo_barista': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Barista del Mes - Noviembre 2025'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'imagen': 'Imagen del Carrusel',
            'orden': 'Orden de Visualización (1-5)',
            'titulo_barista': 'Título/Nombre del Barista del Mes (solo para orden 1)',
            'activo': 'Activo'
        }


class EventoForm(forms.ModelForm):
    """Formulario para gestionar eventos"""
    
    imagen = forms.ImageField(
        required=False,
        validators=[validar_imagen_evento_noticia],
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/jpeg,image/jpg,image/png'
        }),
        label='Imagen del Evento (opcional)'
    )
    
    eliminar_imagen = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Eliminar imagen actual'
    )
    
    class Meta:
        model = Evento
        fields = ['titulo', 'descripcion', 'fecha_evento', 'imagen', 'activo']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del evento'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '4',
                'placeholder': 'Descripción del evento'
            }),
            'fecha_evento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'titulo': 'Título del Evento',
            'descripcion': 'Descripción',
            'fecha_evento': 'Fecha del Evento',
            'activo': 'Activo'
        }


class NoticiaForm(forms.ModelForm):
    """Formulario para gestionar noticias"""
    
    imagen = forms.ImageField(
        required=False,
        validators=[validar_imagen_evento_noticia],
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/jpeg,image/jpg,image/png'
        }),
        label='Imagen de la Noticia (opcional)'
    )
    
    eliminar_imagen = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Eliminar imagen actual'
    )
    
    class Meta:
        model = Noticia
        fields = ['titulo', 'descripcion', 'fecha_publicacion', 'imagen', 'activo']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título de la noticia'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '4',
                'placeholder': 'Descripción de la noticia'
            }),
            'fecha_publicacion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'titulo': 'Título de la Noticia',
            'descripcion': 'Descripción',
            'fecha_publicacion': 'Fecha de Publicación',
            'activo': 'Activo'
        }


class ContactoForm(forms.ModelForm):
    """Formulario para gestionar contactos"""
    
    imagen = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/jpeg,image/jpg,image/png'
        }),
        label='Imagen del Contacto (opcional)'
    )
    
    eliminar_imagen = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Eliminar imagen actual'
    )
    
    class Meta:
        model = Contacto
        fields = ['nombre', 'cargo', 'email', 'telefono', 'imagen', 'orden', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del contacto'
            }),
            'cargo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cargo del contacto'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56 9 XXXX XXXX'
            }),
            'orden': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'nombre': 'Nombre',
            'cargo': 'Cargo',
            'email': 'Correo Electrónico',
            'telefono': 'Teléfono',
            'orden': 'Orden de Visualización',
            'activo': 'Activo'
        }


class ManualInternoForm(forms.ModelForm):
    """Formulario para gestionar la documentación"""
    
    class Meta:
        model = ManualInterno
        fields = ['titulo', 'tipo', 'archivo', 'activo']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del documento'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'archivo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'titulo': 'Título del Documento',
            'tipo': 'Tipo de Documento',
            'archivo': 'Archivo del Documento (PDF, DOC, DOCX)',
            'activo': 'Activo'
        }


class ContactoForm(forms.ModelForm):
    """Formulario para gestionar contactos"""
    
    imagen = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/jpeg,image/jpg,image/png'
        }),
        label='Imagen del Contacto (opcional)'
    )
    
    eliminar_imagen = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Eliminar imagen actual'
    )
    
    class Meta:
        model = Contacto
        fields = ['nombre', 'cargo', 'email', 'telefono', 'imagen', 'orden', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            }),
            'cargo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cargo o puesto'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56 9 XXXX XXXX'
            }),
            'orden': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'nombre': 'Nombre',
            'cargo': 'Cargo',
            'email': 'Correo Electrónico',
            'telefono': 'Teléfono',
            'orden': 'Orden de Visualización',
            'activo': 'Activo'
        }
