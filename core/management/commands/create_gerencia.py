"""
Comando de Django para crear el usuario administrador Gerencia
Ejecutar con: python manage.py create_gerencia
"""
from django.core.management.base import BaseCommand
from core.models import Usuario


class Command(BaseCommand):
    help = 'Crea el usuario administrador Gerencia'

    def handle(self, *args, **options):
        if not Usuario.objects.filter(username='Gerencia').exists():
            usuario = Usuario.objects.create_user(
                username='Gerencia',
                password='Ger_2O25',
                rol='admin',
                is_staff=True,
                is_superuser=True,
                activo=True
            )
            self.stdout.write(
                self.style.SUCCESS(f'Usuario administrador "Gerencia" creado exitosamente')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'El usuario "Gerencia" ya existe')
            )




