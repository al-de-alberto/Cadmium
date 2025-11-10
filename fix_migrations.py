"""
Script para corregir el historial de migraciones
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cadmium.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    # Eliminar registros de migraciones de admin que causan el problema
    cursor.execute("DELETE FROM django_migrations WHERE app = 'admin' AND name LIKE '0001%'")
    cursor.execute("DELETE FROM django_migrations WHERE app = 'contenttypes' AND name LIKE '0001%'")
    cursor.execute("DELETE FROM django_migrations WHERE app = 'auth' AND name LIKE '0001%'")
    print("Migraciones problemáticas eliminadas")
    print("Ahora ejecuta: python manage.py migrate")















