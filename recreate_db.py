"""
Script para eliminar y recrear la base de datos completamente
"""
import os
import sqlite3

db_path = 'db.sqlite3'

if os.path.exists(db_path):
    try:
        # Intentar cerrar cualquier conexión abierta
        conn = sqlite3.connect(db_path)
        conn.close()
        
        # Eliminar el archivo
        os.remove(db_path)
        print(f"Base de datos {db_path} eliminada exitosamente")
        print("Ahora ejecuta: python manage.py migrate")
    except PermissionError:
        print(f"Error: No se puede eliminar {db_path} porque esta en uso.")
        print("Por favor cierra el servidor Django y cualquier herramienta que use la base de datos")
    except Exception as e:
        print(f"Error: {e}")
else:
    print("No se encontro db.sqlite3")















