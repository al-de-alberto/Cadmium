# Instrucciones para Subir el Proyecto a GitHub

## Repositorio Existente: Cadmium-kanban-proyecto-ev2

El repositorio ya existe en GitHub: **https://github.com/99milo/Cadmium-kanban-proyecto-ev2**

## Paso 1: Verificar que Git esté instalado

Abre PowerShell o CMD y ejecuta:
```powershell
git --version
```

Si no está instalado, descárgalo desde: https://git-scm.com/download/win

## Paso 2: Inicializar Git en el proyecto local

Abre PowerShell o CMD en la carpeta del proyecto y ejecuta:

```powershell
cd "c:\0 INACAP\Cuarto Semestre\Ingenieria de Software\Cadmium"

# Inicializar el repositorio (si no está inicializado)
git init

# Agregar todos los archivos
git add .

# Hacer el primer commit
git commit -m "Actualización: Sistema CADMIUM con página principal, carrusel, noticias y página de contacto"
```

## Paso 3: Conectar con el repositorio existente

```powershell
# Agregar el repositorio remoto
git remote add origin https://github.com/99milo/Cadmium-kanban-proyecto-ev2.git

# Verificar que se agregó correctamente
git remote -v
```

**Si ya tenías un remoto configurado**, puedes actualizarlo:

```powershell
# Ver remotos actuales
git remote -v

# Actualizar la URL del remoto
git remote set-url origin https://github.com/99milo/Cadmium-kanban-proyecto-ev2.git
```

## Paso 4: Sincronizar con el repositorio remoto

**IMPORTANTE**: Si el repositorio remoto ya tiene código, primero debes hacer pull:

```powershell
# Traer cambios del repositorio remoto (si hay)
git pull origin main --allow-unrelated-histories
```

O si la rama se llama `master`:

```powershell
git pull origin master --allow-unrelated-histories
```

Si hay conflictos, resuélvelos y luego continúa. Si no hay conflictos o después de resolverlos:

```powershell
# Agregar todos los cambios
git add .

# Hacer commit
git commit -m "Actualización: Sistema CADMIUM con página principal, carrusel, noticias y página de contacto"

# Cambiar a la rama main (si es necesario)
git branch -M main

# Subir los cambios
git push -u origin main
```

Si la rama remota se llama `master` en lugar de `main`:

```powershell
git branch -M master
git push -u origin master
```

## Paso 5: Si el repositorio remoto está vacío

Si el repositorio remoto está vacío o es la primera vez que subes código:

```powershell
# Cambiar a la rama main (si es necesario)
git branch -M main

# Subir el código
git push -u origin main
```

## Notas importantes

- El archivo `.gitignore` ya está configurado para excluir:
  - Base de datos SQLite (`db.sqlite3`)
  - Archivos de Python compilados (`__pycache__`)
  - Variables de entorno (`.env`)
  - Carpetas de entorno virtual (`venv/`, `env/`)
  - Archivos SQL (`.sql`)

- **IMPORTANTE**: No subas la base de datos ni archivos sensibles. El `.gitignore` ya los excluye.

- Si tienes problemas de autenticación, GitHub ahora requiere un Personal Access Token en lugar de contraseña.

## Crear Personal Access Token (si es necesario)

1. Ve a GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Genera un nuevo token con permisos `repo`
3. Copia el token y úsalo como contraseña cuando Git te lo pida

## Comandos útiles para futuros cambios

```powershell
# Ver el estado de los archivos
git status

# Ver qué rama estás usando
git branch

# Agregar archivos modificados
git add .

# Hacer commit
git commit -m "Descripción de los cambios"

# Subir cambios
git push

# Ver el historial de commits
git log --oneline
```

## Solución de problemas comunes

### Error: "fatal: remote origin already exists"
```powershell
# Eliminar el remoto existente
git remote remove origin

# Agregar el remoto correcto
git remote add origin https://github.com/99milo/Cadmium-kanban-proyecto-ev2.git
```

### Error: "Updates were rejected because the remote contains work"
```powershell
# Primero hacer pull
git pull origin main --allow-unrelated-histories

# Resolver conflictos si los hay, luego:
git add .
git commit -m "Merge con repositorio remoto"
git push origin main
```
