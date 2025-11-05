from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('contactanos/', views.contactanos_view, name='contactanos'),
    path('panel/', views.panel_view, name='panel'),
    path('panel/usuarios/', views.usuarios_view, name='usuarios'),
    path('panel/inventario/', views.inventario_view, name='inventario'),
    path('panel/asistencia/', views.asistencia_view, name='asistencia'),
]



