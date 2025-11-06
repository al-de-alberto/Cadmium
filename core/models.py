from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ValidationError
import re


def validar_rut_chileno(rut):
    """Valida el formato de RUT chileno"""
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


class Usuario(AbstractUser):
    """Modelo de usuario personalizado"""
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('usuario', 'Usuario'),
    ]
    
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='usuario')
    fecha_creacion = models.DateTimeField(default=timezone.now)
    activo = models.BooleanField(default=True)
    nombre = models.CharField(max_length=20, blank=True, null=True, verbose_name='Nombre')
    apellido = models.CharField(max_length=20, blank=True, null=True, verbose_name='Apellido')
    rut = models.CharField(max_length=12, unique=True, blank=True, null=True, validators=[validar_rut_chileno], verbose_name='RUT')
    correo_institucional = models.EmailField(blank=True, null=True, verbose_name='Correo Institucional')
    cambio_password_requerido = models.BooleanField(default=True, verbose_name='Cambio de Contraseña Requerido')
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return self.username
    
    def es_administrador(self):
        return self.rol == 'admin' or self.is_superuser
    
    def get_nombre_completo(self):
        """Retorna el nombre completo del usuario"""
        if self.nombre and self.apellido:
            return f"{self.nombre} {self.apellido}"
        return self.username


class Inventario(models.Model):
    """Modelo para gestionar el inventario"""
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    cantidad = models.IntegerField(default=0)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    categoria = models.CharField(max_length=100, blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'
        ordering = ['-fecha_actualizacion']
    
    def __str__(self):
        return f"{self.nombre} - Cantidad: {self.cantidad}"


class Asistencia(models.Model):
    """Modelo para gestionar la asistencia"""
    ESTADO_CHOICES = [
        ('presente', 'Presente'),
        ('ausente', 'Ausente'),
        ('tarde', 'Tarde'),
        ('justificado', 'Justificado'),
    ]
    
    TURNO_CHOICES = [
        ('apertura', 'Apertura (09:00 - 13:00)'),
        ('tarde', 'Tarde (13:00 - 17:00)'),
        ('cierre', 'Cierre (17:00 - 21:00)'),
    ]
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='asistencias')
    fecha = models.DateField(default=timezone.now)
    hora_entrada = models.TimeField(null=True, blank=True)
    hora_salida = models.TimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='presente')
    turno = models.CharField(max_length=20, choices=TURNO_CHOICES, blank=True, null=True, verbose_name='Turno')
    observaciones = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        ordering = ['-fecha', '-fecha_registro']
        unique_together = ['usuario', 'fecha']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.fecha} - {self.get_estado_display()}"


class RegistroFalla(models.Model):
    """Modelo para registrar fallas en las máquinas"""
    
    contador_falla = models.IntegerField(verbose_name='Contador de Falla', unique=True)
    fecha = models.DateField(default=timezone.now, verbose_name='Fecha')
    maquina = models.CharField(max_length=200, verbose_name='Código de Máquina')
    descripcion = models.TextField(verbose_name='Descripción de la Falla')
    observaciones = models.TextField(blank=True, verbose_name='Observaciones')
    fecha_registro = models.DateTimeField(default=timezone.now, verbose_name='Fecha de Registro')
    usuario_registro = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='fallas_registradas', verbose_name='Usuario que Registra')
    
    class Meta:
        verbose_name = 'Registro de Falla'
        verbose_name_plural = 'Registros de Fallas'
        ordering = ['-fecha', '-contador_falla']
    
    def __str__(self):
        return f"Falla #{self.contador_falla} - {self.maquina} - {self.fecha}"


class RegistroLlamada(models.Model):
    """Modelo para registrar llamadas al técnico"""
    
    contador_llamada = models.IntegerField(verbose_name='Contador de Llamada', unique=True)
    fecha = models.DateField(default=timezone.now, verbose_name='Fecha')
    motivo = models.CharField(max_length=200, verbose_name='Motivo de la Llamada')
    tecnico_contactado = models.CharField(max_length=200, verbose_name='Técnico Contactado')
    descripcion = models.TextField(verbose_name='Descripción')
    observaciones = models.TextField(blank=True, verbose_name='Observaciones')
    fecha_registro = models.DateTimeField(default=timezone.now, verbose_name='Fecha de Registro')
    usuario_registro = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='llamadas_registradas', verbose_name='Usuario que Registra')
    
    class Meta:
        verbose_name = 'Registro de Llamada'
        verbose_name_plural = 'Registros de Llamadas'
        ordering = ['-fecha', '-contador_llamada']
    
    def __str__(self):
        return f"Llamada #{self.contador_llamada} - {self.motivo} - {self.fecha}"




