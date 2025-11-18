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
    """Modelo de usuario personalizado con roles múltiples"""
    fecha_creacion = models.DateTimeField(default=timezone.now)
    activo = models.BooleanField(default=True)
    nombre = models.CharField(max_length=20, blank=True, null=True, verbose_name='Nombre')
    apellido = models.CharField(max_length=20, blank=True, null=True, verbose_name='Apellido')
    rut = models.CharField(max_length=12, unique=True, blank=True, null=True, validators=[validar_rut_chileno], verbose_name='RUT')
    correo_institucional = models.EmailField(blank=True, null=True, verbose_name='Correo Institucional')
    cambio_password_requerido = models.BooleanField(default=True, verbose_name='Cambio de Contraseña Requerido')
    
    # Roles múltiples - un usuario puede ser Administrador y/o Colaborador
    _es_administrador = models.BooleanField(default=False, verbose_name='Es Administrador', db_column='es_administrador')
    es_colaborador = models.BooleanField(default=True, verbose_name='Es Colaborador')
    
    # Mantener el campo 'rol' para compatibilidad con migraciones existentes (deprecated)
    rol = models.CharField(max_length=20, blank=True, null=True, verbose_name='Rol (deprecated)')
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return self.username
    
    @property
    def es_administrador(self):
        """Property para acceder al campo es_administrador"""
        return self._es_administrador
    
    @es_administrador.setter
    def es_administrador(self, value):
        """Setter para el campo es_administrador"""
        self._es_administrador = value
    
    def get_roles_display(self):
        """Retorna una lista de roles activos del usuario"""
        roles = []
        if self._es_administrador or self.is_superuser:
            roles.append('Administrador')
        if self.es_colaborador:
            roles.append('Colaborador')
        return ', '.join(roles) if roles else 'Sin rol asignado'
    
    def get_nombre_completo(self):
        """Retorna el nombre completo del usuario"""
        if self.nombre and self.apellido:
            return f"{self.nombre} {self.apellido}"
        return self.username
    
    # Método para compatibilidad con código existente
    def tiene_permisos_administrador(self):
        """Retorna True si el usuario tiene permisos de administrador"""
        return self._es_administrador or self.is_superuser


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
    codigo = models.CharField(max_length=200, verbose_name='Código del Pedido')
    fecha_creacion = models.DateTimeField(default=timezone.now, verbose_name='Fecha de Creación')
    usuario_creacion = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos_creados', verbose_name='Usuario que Crea')
    observaciones = models.TextField(blank=True, verbose_name='Observaciones')
    
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"Pedido: {self.codigo} - {self.fecha_creacion.strftime('%d/%m/%Y %H:%M')}"


class DetallePedido(models.Model):
    """Modelo para los detalles de un pedido"""
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles', verbose_name='Pedido')
    producto_nombre = models.CharField(max_length=200, verbose_name='Nombre del Producto')
    cantidad = models.IntegerField(verbose_name='Cantidad')
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Precio Unitario')
    
    class Meta:
        verbose_name = 'Detalle de Pedido'
        verbose_name_plural = 'Detalles de Pedido'
        ordering = ['pedido', 'id']
    
    @property
    def precio_total(self):
        """Calcula el precio total del detalle (cantidad * precio_unitario)"""
        return self.cantidad * self.precio_unitario
    
    def __str__(self):
        return f"{self.producto_nombre} - Cantidad: {self.cantidad} - Precio: ${self.precio_unitario}"


class Auditoria(models.Model):
    """Modelo para registrar todas las acciones del sistema"""
    ACCION_CHOICES = [
        ('login', 'Inicio de Sesión'),
        ('logout', 'Cierre de Sesión'),
        ('login_failed', 'Intento de Login Fallido'),
        ('password_change', 'Cambio de Contraseña'),
        ('password_reset_request', 'Solicitud de Restablecimiento de Contraseña'),
        ('password_reset_admin', 'Restablecimiento de Contraseña por Admin'),
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
        ('carrusel_create', 'Creación de Imagen Carrusel'),
        ('carrusel_edit', 'Edición de Imagen Carrusel'),
        ('carrusel_delete', 'Eliminación de Imagen Carrusel'),
        ('evento_create', 'Creación de Evento'),
        ('evento_edit', 'Edición de Evento'),
        ('evento_delete', 'Eliminación de Evento'),
        ('noticia_create', 'Creación de Noticia'),
        ('noticia_edit', 'Edición de Noticia'),
        ('noticia_delete', 'Eliminación de Noticia'),
        ('falla_create', 'Registro de Falla'),
        ('falla_edit', 'Edición de Falla'),
        ('falla_delete', 'Eliminación de Falla'),
        ('llamada_create', 'Registro de Llamada'),
        ('llamada_edit', 'Edición de Llamada'),
        ('llamada_delete', 'Eliminación de Llamada'),
        ('contacto_create', 'Creación de Contacto'),
        ('contacto_edit', 'Edición de Contacto'),
        ('contacto_delete', 'Eliminación de Contacto'),
    ]
    
    MODULO_CHOICES = [
        ('sesion', 'Sesión'),
        ('usuarios', 'Usuarios'),
        ('inventario', 'Inventario'),
        ('asistencia', 'Asistencia'),
        ('pedidos', 'Ventas y Pedidos'),
        ('operaciones', 'Operaciones'),
        ('contenido', 'Contenido'),
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


class ImagenCarrusel(models.Model):
    """Modelo para gestionar las imágenes del carrusel"""
    imagen = models.ImageField(upload_to='carousel/', verbose_name='Imagen del Carrusel')
    orden = models.IntegerField(default=0, verbose_name='Orden de Visualización')
    titulo_barista = models.CharField(max_length=200, blank=True, null=True, verbose_name='Título/Nombre del Barista del Mes (solo para orden 1)')
    activo = models.BooleanField(default=True, verbose_name='Activo')
    fecha_creacion = models.DateTimeField(default=timezone.now, verbose_name='Fecha de Creación')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')
    
    class Meta:
        verbose_name = 'Imagen del Carrusel'
        verbose_name_plural = 'Imágenes del Carrusel'
        ordering = ['orden', 'fecha_creacion']
    
    def __str__(self):
        if self.orden == 1 and self.titulo_barista:
            return f"Barista del Mes: {self.titulo_barista} - {'Activa' if self.activo else 'Inactiva'}"
        return f"Imagen Carrusel #{self.orden} - {'Activa' if self.activo else 'Inactiva'}"
    
    def es_barista_mes(self):
        """Indica si esta imagen es para el barista del mes (orden 1)"""
        return self.orden == 1


class Evento(models.Model):
    """Modelo para gestionar eventos del PopUp"""
    titulo = models.CharField(max_length=200, verbose_name='Título del Evento')
    descripcion = models.TextField(verbose_name='Descripción')
    fecha_evento = models.DateField(verbose_name='Fecha del Evento')
    imagen = models.ImageField(upload_to='eventos/', blank=True, null=True, verbose_name='Imagen del Evento')
    activo = models.BooleanField(default=True, verbose_name='Activo')
    fecha_creacion = models.DateTimeField(default=timezone.now, verbose_name='Fecha de Creación')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')
    
    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['-fecha_evento', '-fecha_creacion']
    
    def __str__(self):
        return f"{self.titulo} - {self.fecha_evento.strftime('%d/%m/%Y')}"


class Noticia(models.Model):
    """Modelo para gestionar noticias y actualizaciones"""
    titulo = models.CharField(max_length=200, verbose_name='Título de la Noticia')
    descripcion = models.TextField(verbose_name='Descripción')
    fecha_publicacion = models.DateField(default=timezone.now, verbose_name='Fecha de Publicación')
    imagen = models.ImageField(upload_to='noticias/', blank=True, null=True, verbose_name='Imagen de la Noticia')
    activo = models.BooleanField(default=True, verbose_name='Activo')
    fecha_creacion = models.DateTimeField(default=timezone.now, verbose_name='Fecha de Creación')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')
    
    class Meta:
        verbose_name = 'Noticia'
        verbose_name_plural = 'Noticias'
        ordering = ['-fecha_publicacion', '-fecha_creacion']
    
    def __str__(self):
        return f"{self.titulo} - {self.fecha_publicacion.strftime('%d/%m/%Y')}"


class ManualInterno(models.Model):
    """Modelo para el manual interno (reglamento interno y manual de operaciones)"""
    TIPO_CHOICES = [
        ('reglamento', 'Reglamento Interno'),
        ('operaciones', 'Manual de Operaciones'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name='Título del Documento')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='reglamento', verbose_name='Tipo de Documento')
    archivo = models.FileField(upload_to='manuales/', verbose_name='Archivo del Documento')
    fecha_creacion = models.DateTimeField(default=timezone.now, verbose_name='Fecha de Creación')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')
    activo = models.BooleanField(default=True, verbose_name='Activo')
    
    class Meta:
        verbose_name = 'Documentación'
        verbose_name_plural = 'Documentación'
        ordering = ['-fecha_actualizacion']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.titulo}"


class Contacto(models.Model):
    """Modelo para los contactos de gerencia"""
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    cargo = models.CharField(max_length=200, verbose_name='Cargo')
    email = models.EmailField(verbose_name='Correo Electrónico')
    telefono = models.CharField(max_length=20, verbose_name='Teléfono')
    imagen = models.ImageField(upload_to='contactos/', blank=True, null=True, verbose_name='Imagen')
    orden = models.IntegerField(default=0, verbose_name='Orden de Visualización')
    activo = models.BooleanField(default=True, verbose_name='Activo')
    fecha_creacion = models.DateTimeField(default=timezone.now, verbose_name='Fecha de Creación')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')
    
    class Meta:
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'
        ordering = ['orden', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.cargo}"


