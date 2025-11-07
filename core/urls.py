from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cambiar-password/', views.cambiar_password_view, name='cambiar_password'),
    path('contactanos/', views.contactanos_view, name='contactanos'),
    path('trabajador/dashboard/', views.trabajador_dashboard_view, name='trabajador_dashboard'),
    path('trabajador/registro-asistencia/', views.registro_asistencia_view, name='registro_asistencia'),
    path('trabajador/cambiar-stock/', views.cambiar_stock_view, name='cambiar_stock'),
    path('trabajador/actualizar-stock/<int:producto_id>/', views.actualizar_stock_view, name='actualizar_stock'),
    path('panel/', views.panel_view, name='panel'),
    path('panel/usuarios/', views.usuarios_view, name='usuarios'),
    path('panel/usuarios/crear/', views.crear_usuario_view, name='crear_usuario'),
    path('panel/usuarios/editar/<int:usuario_id>/', views.editar_usuario_view, name='editar_usuario'),
    path('panel/usuarios/eliminar/<int:usuario_id>/', views.eliminar_usuario_view, name='eliminar_usuario'),
    path('panel/inventario/', views.inventario_view, name='inventario'),
    path('panel/inventario/crear/', views.crear_inventario_view, name='crear_inventario'),
    path('panel/inventario/editar/<int:producto_id>/', views.editar_inventario_view, name='editar_inventario'),
    path('panel/inventario/eliminar/<int:producto_id>/', views.eliminar_inventario_view, name='eliminar_inventario'),
    path('panel/asistencia/', views.asistencia_view, name='asistencia'),
    path('panel/ventas-pedidos/', views.ventas_pedidos_view, name='ventas_pedidos'),
    path('panel/ventas-pedidos/crear/', views.crear_pedido_view, name='crear_pedido'),
    path('panel/ventas-pedidos/exportar/<int:pedido_id>/', views.exportar_pedido_excel, name='exportar_pedido_excel'),
    path('panel/ventas-pedidos/eliminar/<int:pedido_id>/', views.eliminar_pedido_view, name='eliminar_pedido'),
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
    path('panel/auditoria/', views.auditoria_view, name='auditoria'),
]



