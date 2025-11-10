"""
Script para marcar todas las migraciones necesarias como aplicadas
"""
import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

try:
    # Obtener todas las migraciones que deberían estar aplicadas
    migrations_needed = [
        ('contenttypes', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0001_initial'),
        ('auth', '0002_alter_permission_name_max_length'),
        ('auth', '0003_alter_user_email_max_length'),
        ('auth', '0004_alter_user_username_opts'),
        ('auth', '0005_alter_user_last_login_null'),
        ('auth', '0006_require_contenttypes_0002'),
        ('auth', '0007_alter_validators_add_error_messages'),
        ('auth', '0008_alter_user_username_max_length'),
        ('auth', '0009_alter_user_last_name_max_length'),
        ('auth', '0010_alter_group_name_max_length'),
        ('auth', '0011_update_proxy_permissions'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('admin', '0001_initial'),
        ('admin', '0002_logentry_remove_auto_add'),
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('sessions', '0001_initial'),
        ('core', '0001_initial'),
    ]
    
    for app, name in migrations_needed:
        cursor.execute("""
            INSERT OR IGNORE INTO django_migrations (app, name, applied)
            VALUES (?, ?, datetime('now'))
        """, (app, name))
    
    conn.commit()
    print(f"Marcadas {len(migrations_needed)} migraciones como aplicadas")
    print("Verifica con: python manage.py showmigrations")
    
except Exception as e:
    print(f"Error: {e}")
    conn.rollback()
finally:
    conn.close()















