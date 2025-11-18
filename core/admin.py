from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario, Inventario, Asistencia, Pedido, DetallePedido, Auditoria


@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'get_roles_display', 'activo', 'fecha_creacion']
    list_filter = ['_es_administrador', 'es_colaborador', 'activo', 'is_superuser']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información Adicional', {'fields': ('_es_administrador', 'es_colaborador', 'activo', 'fecha_creacion')}),
    )
    readonly_fields = ['fecha_creacion']


@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'cantidad', 'precio_unitario', 'fecha_actualizacion']
    list_filter = ['categoria', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion', 'categoria']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']


@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'fecha', 'estado', 'hora_entrada', 'hora_salida']
    list_filter = ['estado', 'fecha', 'usuario']
    search_fields = ['usuario__username', 'observaciones']
    readonly_fields = ['fecha_registro']


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 1


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'fecha_creacion', 'usuario_creacion']
    list_filter = ['fecha_creacion']
    search_fields = ['codigo', 'observaciones']
    readonly_fields = ['fecha_creacion']
    inlines = [DetallePedidoInline]


@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ['fecha_hora', 'usuario', 'accion', 'modulo', 'objeto_afectado']
    list_filter = ['modulo', 'accion', 'fecha_hora', 'usuario']
    search_fields = ['usuario__username', 'usuario__nombre', 'usuario__apellido', 'descripcion', 'objeto_afectado']
    readonly_fields = ['fecha_hora']
    date_hierarchy = 'fecha_hora'
    ordering = ['-fecha_hora']
    
    def has_add_permission(self, request):
        # No permitir agregar registros manualmente
        return False
    
    def has_change_permission(self, request, obj=None):
        # No permitir modificar registros de auditoría
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Solo superusuarios pueden eliminar registros de auditoría
        return request.user.is_superuser




