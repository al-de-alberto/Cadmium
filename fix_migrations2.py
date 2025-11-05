"""
Script para corregir el orden de las migraciones
"""
import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

try:
    # Eliminar el registro de core.0001_initial
    cursor.execute("DELETE FROM django_migrations WHERE app='core' AND name='0001_initial'")
    
    # Asegurar que auth.0012 esté registrado
    cursor.execute("""
        INSERT OR IGNORE INTO django_migrations (app, name, applied)
        VALUES ('auth', '0012_alter_user_first_name_max_length', datetime('now'))
    """)
    
    conn.commit()
    print("Migraciones corregidas")
    print("Ahora ejecuta: python manage.py migrate --fake core")
    
except Exception as e:
    print(f"Error: {e}")
    conn.rollback()
finally:
    conn.close()



