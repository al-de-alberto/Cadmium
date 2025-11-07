"""
Script para crear manualmente las tablas de core que faltan
"""
import sqlite3
import os

db_path = 'db.sqlite3'

if not os.path.exists(db_path):
    print("No se encontro db.sqlite3")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Verificar si la tabla core_usuario ya existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='core_usuario'")
    if cursor.fetchone():
        print("La tabla core_usuario ya existe")
    else:
        # Crear la tabla core_usuario
        cursor.execute("""
            CREATE TABLE "core_usuario" (
                "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                "password" varchar(128) NOT NULL,
                "last_login" datetime NULL,
                "is_superuser" bool NOT NULL,
                "username" varchar(150) NOT NULL UNIQUE,
                "first_name" varchar(150) NOT NULL,
                "last_name" varchar(150) NOT NULL,
                "email" varchar(254) NOT NULL,
                "is_staff" bool NOT NULL,
                "is_active" bool NOT NULL,
                "date_joined" datetime NOT NULL,
                "rol" varchar(20) NOT NULL,
                "fecha_creacion" datetime NOT NULL,
                "activo" bool NOT NULL
            )
        """)
        
        # Crear tabla core_inventario
        cursor.execute("""
            CREATE TABLE "core_inventario" (
                "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                "nombre" varchar(200) NOT NULL,
                "descripcion" text NOT NULL,
                "cantidad" integer NOT NULL,
                "precio_unitario" decimal NOT NULL,
                "categoria" varchar(100) NOT NULL,
                "fecha_creacion" datetime NOT NULL,
                "fecha_actualizacion" datetime NOT NULL
            )
        """)
        
        # Crear tabla core_asistencia
        cursor.execute("""
            CREATE TABLE "core_asistencia" (
                "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                "fecha" date NOT NULL,
                "hora_entrada" time NULL,
                "hora_salida" time NULL,
                "estado" varchar(20) NOT NULL,
                "observaciones" text NOT NULL,
                "fecha_registro" datetime NOT NULL,
                "usuario_id" bigint NOT NULL REFERENCES "core_usuario" ("id") DEFERRABLE INITIALLY DEFERRED
            )
        """)
        
        # Crear índices
        cursor.execute('CREATE UNIQUE INDEX "core_asistencia_usuario_id_fecha_abc123" ON "core_asistencia" ("usuario_id", "fecha")')
        cursor.execute('CREATE INDEX "core_asistencia_usuario_id_xyz789" ON "core_asistencia" ("usuario_id")')
        
        # Registrar la migración
        cursor.execute("""
            INSERT INTO django_migrations (app, name, applied)
            VALUES ('core', '0001_initial', datetime('now'))
        """)
        
        conn.commit()
        print("Tablas de core creadas exitosamente")
        print("Migracion registrada en django_migrations")
        
except sqlite3.OperationalError as e:
    if "already exists" in str(e).lower():
        print("Algunas tablas ya existen, continuando...")
        conn.commit()
    else:
        print(f"Error: {e}")
        conn.rollback()
except Exception as e:
    print(f"Error: {e}")
    conn.rollback()
finally:
    conn.close()





