"""
Script para crear el usuario administrador Gerencia
Ejecutar con: python manage.py shell < create_admin.py
O mejor: python manage.py createsuperuser (manual)
"""

from core.models import Usuario

# Crear usuario administrador si no existe
if not Usuario.objects.filter(username='Gerencia').exists():
    usuario = Usuario.objects.create_user(
        username='Gerencia',
        password='Ger_2O25',
        rol='admin',
        is_staff=True,
        is_superuser=True,
        activo=True,
        cambio_password_requerido=False  # Los administradores no necesitan cambiar contraseña
    )
    print(f'Usuario administrador "Gerencia" creado exitosamente')
else:
    print(f'El usuario "Gerencia" ya existe')




