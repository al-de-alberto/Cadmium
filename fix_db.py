"""
Script para corregir el historial de migraciones eliminando las entradas problemáticas
"""
import sqlite3
import os

db_path = 'db.sqlite3'

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Eliminar todas las migraciones aplicadas para poder empezar de nuevo
        cursor.execute("DELETE FROM django_migrations")
        print("Historial de migraciones limpiado")
        
        conn.commit()
        print("Cambios guardados")
        print("\nAhora ejecuta: python manage.py migrate")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()
else:
    print("No se encontró db.sqlite3")

