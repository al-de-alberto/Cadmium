from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ValidationError
import re


def validar_rut_chileno(rut):
    """Valida el formato de RUT chileno (solo formato, no dígito verificador matemático)"""
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
    CATEGORIA_CHOICES = [
        ('bodega', 'Bodega'),
        ('meson', 'Mesón'),
        ('limpieza', 'Limpieza'),
    ]
    
    nombre = models.CharField(max_length=200, verbose_name='Nombre del Producto')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    cantidad = models.IntegerField(default=0, verbose_name='Cantidad')
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Precio Unitario')
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, verbose_name='Categoría')
    imagen = models.ImageField(upload_to='inventario/', blank=True, null=True, verbose_name='Imagen del Producto')
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Producto de Inventario'
        verbose_name_plural = 'Productos de Inventario'
        ordering = ['categoria', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.get_categoria_display()}) - Cantidad: {self.cantidad}"


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


class Pedido(models.Model):
    """Modelo para gestionar pedidos"""
    nombre = models.CharField(max_length=200, verbose_name='Nombre del Pedido')
    fecha_creacion = models.DateTimeField(default=timezone.now, verbose_name='Fecha de Creación')
    usuario_creacion = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos_creados', verbose_name='Usuario que Crea')
    observaciones = models.TextField(blank=True, verbose_name='Observaciones')
    
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"Pedido: {self.nombre} - {self.fecha_creacion.strftime('%d/%m/%Y %H:%M')}"


class DetallePedido(models.Model):
    """Modelo para los detalles de un pedido"""
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles', verbose_name='Pedido')
    producto_nombre = models.CharField(max_length=200, verbose_name='Nombre del Producto')
    cantidad = models.IntegerField(verbose_name='Cantidad')
    
    class Meta:
        verbose_name = 'Detalle de Pedido'
        verbose_name_plural = 'Detalles de Pedido'
        ordering = ['pedido', 'id']
    
    def __str__(self):
        return f"{self.producto_nombre} - Cantidad: {self.cantidad}"


class Auditoria(models.Model):
    """Modelo para registrar todas las acciones del sistema"""
    ACCION_CHOICES = [
        ('login', 'Inicio de Sesión'),
        ('logout', 'Cierre de Sesión'),
        ('login_failed', 'Intento de Login Fallido'),
        ('password_change', 'Cambio de Contraseña'),
        ('usuario_create', 'Creación de Usuario'),
        ('usuario_edit', 'Edición de Usuario'),
        ('usuario_delete', 'Eliminación de Usuario'),
        ('usuario_activate', 'Activación de Usuario'),
        ('usuario_deactivate', 'Desactivación de Usuario'),
        ('inventario_create', 'Creación de Producto'),
        ('inventario_edit', 'Edición de Producto'),
        ('inventario_delete', 'Eliminación de Producto'),
        ('inventario_stock_change', 'Cambio de Stock'),
        ('asistencia_create', 'Registro de Asistencia'),
        ('asistencia_edit', 'Edición de Asistencia'),
        ('asistencia_delete', 'Eliminación de Asistencia'),
        ('pedido_create', 'Creación de Pedido'),
        ('pedido_delete', 'Eliminación de Pedido'),
        ('pedido_export', 'Exportación de Pedido'),
        ('falla_create', 'Registro de Falla'),
        ('falla_edit', 'Edición de Falla'),
        ('falla_delete', 'Eliminación de Falla'),
        ('llamada_create', 'Registro de Llamada'),
        ('llamada_edit', 'Edición de Llamada'),
        ('llamada_delete', 'Eliminación de Llamada'),
    ]
    
    MODULO_CHOICES = [
        ('sesion', 'Sesión'),
        ('usuarios', 'Usuarios'),
        ('inventario', 'Inventario'),
        ('asistencia', 'Asistencia'),
        ('pedidos', 'Ventas y Pedidos'),
        ('operaciones', 'Operaciones'),
    ]
    
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='auditorias', verbose_name='Usuario')
    accion = models.CharField(max_length=50, choices=ACCION_CHOICES, verbose_name='Acción')
    modulo = models.CharField(max_length=50, choices=MODULO_CHOICES, verbose_name='Módulo')
    descripcion = models.TextField(verbose_name='Descripción')
    detalles = models.TextField(blank=True, null=True, verbose_name='Detalles Adicionales (JSON)')
    fecha_hora = models.DateTimeField(default=timezone.now, verbose_name='Fecha y Hora')
    objeto_afectado = models.CharField(max_length=200, blank=True, null=True, verbose_name='Objeto Afectado')
    
    class Meta:
        verbose_name = 'Registro de Auditoría'
        verbose_name_plural = 'Registros de Auditoría'
        ordering = ['-fecha_hora']
        indexes = [
            models.Index(fields=['-fecha_hora']),
            models.Index(fields=['usuario']),
            models.Index(fields=['modulo']),
            models.Index(fields=['accion']),
        ]
    
    def __str__(self):
        usuario_nombre = self.usuario.get_nombre_completo() if self.usuario else 'Usuario Anónimo'
        return f"{usuario_nombre} - {self.get_accion_display()} - {self.fecha_hora.strftime('%d/%m/%Y %H:%M:%S')}"




