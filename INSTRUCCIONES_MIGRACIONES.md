# Instrucciones para Solucionar el Problema de Migraciones

El error ocurre porque se aplicaron migraciones de Django antes de crear el modelo personalizado de Usuario.

## Solución Rápida:

1. **Cierra cualquier proceso que esté usando la base de datos** (servidor Django, pgAdmin, etc.)

2. **Elimina el archivo `db.sqlite3`**:
   ```powershell
   Remove-Item db.sqlite3
   ```

3. **Ejecuta las migraciones de nuevo**:
   ```powershell
   python manage.py migrate
   ```

4. **Crea el usuario administrador**:
   ```powershell
   python manage.py create_gerencia
   ```

5. **Inicia el servidor**:
   ```powershell
   python manage.py runserver
   ```

## Si el problema persiste:

Si no puedes eliminar `db.sqlite3` porque está en uso:
- Cierra todas las ventanas de PowerShell donde corre el servidor
- Cierra Django Admin o cualquier herramienta de base de datos
- Vuelve a intentar eliminar el archivo



