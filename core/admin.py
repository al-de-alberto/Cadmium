from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario, Inventario, Asistencia


@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'rol', 'activo', 'fecha_creacion']
    list_filter = ['rol', 'activo', 'is_superuser']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información Adicional', {'fields': ('rol', 'activo', 'fecha_creacion')}),
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




