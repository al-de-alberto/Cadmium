from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cambiar-password/', views.cambiar_password_view, name='cambiar_password'),
    path('contactanos/', views.contactanos_view, name='contactanos'),
    path('registro-asistencia/', views.registro_asistencia_view, name='registro_asistencia'),
    path('panel/', views.panel_view, name='panel'),
    path('panel/usuarios/', views.usuarios_view, name='usuarios'),
    path('panel/usuarios/crear/', views.crear_usuario_view, name='crear_usuario'),
    path('panel/usuarios/editar/<int:usuario_id>/', views.editar_usuario_view, name='editar_usuario'),
    path('panel/inventario/', views.inventario_view, name='inventario'),
    path('panel/asistencia/', views.asistencia_view, name='asistencia'),
    path('panel/ventas-pedidos/', views.ventas_pedidos_view, name='ventas_pedidos'),
    path('panel/deliverys/', views.deliverys_view, name='deliverys'),
    path('panel/operaciones/', views.operaciones_view, name='operaciones'),
    path('panel/operaciones/fallas/crear/', views.crear_falla_view, name='crear_falla'),
    path('panel/operaciones/fallas/editar/<int:falla_id>/', views.editar_falla_view, name='editar_falla'),
    path('panel/operaciones/fallas/eliminar/<int:falla_id>/', views.eliminar_falla_view, name='eliminar_falla'),
    path('panel/operaciones/llamadas/crear/', views.crear_llamada_view, name='crear_llamada'),
    path('panel/operaciones/llamadas/editar/<int:llamada_id>/', views.editar_llamada_view, name='editar_llamada'),
    path('panel/operaciones/llamadas/eliminar/<int:llamada_id>/', views.eliminar_llamada_view, name='eliminar_llamada'),
    path('panel/asistencia/editar/<int:asistencia_id>/', views.editar_asistencia_view, name='editar_asistencia'),
    path('panel/asistencia/eliminar/<int:asistencia_id>/', views.eliminar_asistencia_view, name='eliminar_asistencia'),
]



