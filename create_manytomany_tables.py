"""
Script para crear las tablas ManyToMany que faltan
"""
import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

try:
    # Crear tabla core_usuario_groups
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS "core_usuario_groups" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "usuario_id" bigint NOT NULL REFERENCES "core_usuario" ("id") DEFERRABLE INITIALLY DEFERRED,
            "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED
        )
    """)
    
    # Crear tabla core_usuario_user_permissions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS "core_usuario_user_permissions" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "usuario_id" bigint NOT NULL REFERENCES "core_usuario" ("id") DEFERRABLE INITIALLY DEFERRED,
            "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED
        )
    """)
    
    # Crear índices únicos
    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS "core_usuario_groups_usuario_id_group_id_abc123" 
        ON "core_usuario_groups" ("usuario_id", "group_id")
    """)
    
    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS "core_usuario_user_permissions_usuario_id_permission_id_xyz789" 
        ON "core_usuario_user_permissions" ("usuario_id", "permission_id")
    """)
    
    conn.commit()
    print("Tablas ManyToMany creadas exitosamente")
    
except sqlite3.OperationalError as e:
    if "already exists" in str(e).lower():
        print("Las tablas ManyToMany ya existen")
    else:
        print(f"Error: {e}")
        conn.rollback()
except Exception as e:
    print(f"Error: {e}")
    conn.rollback()
finally:
    conn.close()















