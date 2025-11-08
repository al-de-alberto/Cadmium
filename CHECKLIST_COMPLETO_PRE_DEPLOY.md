# ✅ Checklist Completo: Pre-Deploy en Render

## 🎯 Repaso Completo de Todo lo Necesario

Este documento contiene un checklist exhaustivo de todo lo que debes verificar y hacer antes del deploy en Render.

---

## 📋 FASE 1: Verificación de Archivos Críticos

### ✅ 1.1 Archivos de Configuración de Render

Verifica que estos archivos existan y estén correctos:

#### `Procfile`
- [ ] ✅ Existe el archivo `Procfile`
- [ ] ✅ Contenido: `web: gunicorn cadmium.wsgi:application`
- [ ] ✅ Sin líneas adicionales innecesarias

**Verificar:**
```bash
cat Procfile
# Debe mostrar: web: gunicorn cadmium.wsgi:application
```

#### `build.sh`
- [ ] ✅ Existe el archivo `build.sh`
- [ ] ✅ Tiene permisos de ejecución (en Linux/Mac: `chmod +x build.sh`)
- [ ] ✅ Contenido correcto:
  ```bash
  #!/usr/bin/env bash
  # exit on error
  set -o errexit
  
  pip install -r requirements.txt
  python manage.py collectstatic --no-input
  python manage.py migrate
  ```

**Verificar:**
```bash
cat build.sh
```

#### `requirements.txt`
- [ ] ✅ Existe el archivo `requirements.txt`
- [ ] ✅ Contiene todas las dependencias necesarias:
  - [ ] Django==4.2.7
  - [ ] psycopg2-binary>=2.9.9
  - [ ] Pillow>=10.3.0
  - [ ] openpyxl>=3.1.2
  - [ ] whitenoise>=6.6.0
  - [ ] gunicorn>=21.2.0
  - [ ] dj-database-url>=2.1.0

**Verificar:**
```bash
cat requirements.txt
```

#### `runtime.txt` (Opcional pero Recomendado)
- [ ] ✅ Existe el archivo `runtime.txt`
- [ ] ✅ Contiene: `python-3.12.7` (o la versión que uses)

**Verificar:**
```bash
cat runtime.txt
```

---

### ✅ 1.2 Configuración de Django

#### `cadmium/settings.py`
- [ ] ✅ `SECRET_KEY` se obtiene de variable de entorno: `os.environ.get('SECRET_KEY', ...)`
- [ ] ✅ `DEBUG` se obtiene de variable de entorno: `os.environ.get('DEBUG', 'True') == 'True'`
- [ ] ✅ `ALLOWED_HOSTS` se configura desde variable de entorno
- [ ] ✅ Base de datos configurada para usar `DATABASE_URL` o variables individuales
- [ ] ✅ WhiteNoise configurado para producción (cuando `DEBUG=False`)
- [ ] ✅ `STATIC_ROOT` configurado: `BASE_DIR / 'staticfiles'`
- [ ] ✅ `MEDIA_ROOT` configurado: `BASE_DIR / 'media'`

**Verificar secciones clave:**
```python
# Debe tener algo como:
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-...')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
if os.environ.get('DATABASE_URL'):
    import dj_database_url
    DATABASES = {'default': dj_database_url.parse(...)}
```

---

### ✅ 1.3 Archivo .gitignore

- [ ] ✅ Existe el archivo `.gitignore`
- [ ] ✅ Excluye `db.sqlite3` (base de datos local)
- [ ] ✅ Excluye `venv/` o `env/` (entorno virtual)
- [ ] ✅ Excluye `__pycache__/` (archivos Python compilados)
- [ ] ✅ Excluye `*.log` (archivos de log)
- [ ] ✅ Excluye `.env` (variables de entorno locales)
- [ ] ✅ Excluye `staticfiles/` (archivos estáticos compilados)
- [ ] ✅ Excluye `media/` (archivos subidos por usuarios)

**Verificar:**
```bash
cat .gitignore
```

---

## 📋 FASE 2: Pruebas Locales

### ✅ 2.1 Verificar que el Servidor Inicia

- [ ] ✅ El servidor inicia sin errores
- [ ] ✅ No hay errores de importación
- [ ] ✅ No hay errores de configuración

**Comando:**
```bash
python manage.py runserver
# Debe iniciar sin errores
# Presiona Ctrl+C para detener
```

---

### ✅ 2.2 Verificar con Django Check

- [ ] ✅ No hay errores de sistema
- [ ] ✅ No hay advertencias críticas
- [ ] ✅ Todas las configuraciones están correctas

**Comando:**
```bash
python manage.py check
# Debe decir: "System check identified no issues (0 silenced)."
```

---

### ✅ 2.3 Verificar Migraciones

- [ ] ✅ No hay migraciones pendientes
- [ ] ✅ Todas las migraciones se aplican correctamente
- [ ] ✅ No hay conflictos de migraciones

**Comandos:**
```bash
# Verificar migraciones pendientes
python manage.py makemigrations --check --dry-run
# No debe mostrar migraciones pendientes

# Aplicar migraciones
python manage.py migrate
# Debe aplicar sin errores
```

---

### ✅ 2.4 Verificar Archivos Estáticos

- [ ] ✅ Los archivos estáticos se recopilan correctamente
- [ ] ✅ No hay errores al recopilar estáticos
- [ ] ✅ Los archivos CSS, JS e imágenes están incluidos

**Comandos:**
```bash
# Simulación (dry-run)
python manage.py collectstatic --dry-run
# Debe mostrar los archivos que se recopilarían

# Recopilación real (opcional, para probar)
python manage.py collectstatic --no-input
# Debe recopilar sin errores
```

---

### ✅ 2.5 Probar Funcionalidades Básicas

- [ ] ✅ La página principal carga correctamente
- [ ] ✅ El login funciona
- [ ] ✅ El admin es accesible (si está configurado)
- [ ] ✅ Los archivos estáticos se cargan (CSS, imágenes)
- [ ] ✅ La base de datos funciona (puedes crear/editar datos)

**Probar manualmente:**
1. Abre http://127.0.0.1:8000/
2. Verifica que la página carga
3. Prueba hacer login
4. Verifica que los estilos se cargan correctamente

---

## 📋 FASE 3: Preparación de Git y GitHub

### ✅ 3.1 Verificar Estado de Git

- [ ] ✅ Git está inicializado en el proyecto
- [ ] ✅ Hay un repositorio remoto configurado (GitHub)
- [ ] ✅ El código está actualizado

**Comandos:**
```bash
# Verificar estado
git status

# Verificar remoto
git remote -v
# Debe mostrar tu repositorio de GitHub
```

---

### ✅ 3.2 Verificar Archivos a Subir

- [ ] ✅ Los archivos sensibles NO están en el staging area
- [ ] ✅ `db.sqlite3` NO está en el staging area
- [ ] ✅ `venv/` NO está en el staging area
- [ ] ✅ `.env` NO está en el staging area
- [ ] ✅ `staticfiles/` NO está en el staging area

**Comando:**
```bash
git status
# Verifica que los archivos excluidos por .gitignore NO aparezcan
```

---

### ✅ 3.3 Hacer Commit Final

- [ ] ✅ Todos los cambios están agregados
- [ ] ✅ El commit tiene un mensaje descriptivo
- [ ] ✅ El código está listo para producción

**Comandos:**
```bash
# Agregar todos los cambios
git add .

# Verificar qué se va a commitear
git status

# Hacer commit
git commit -m "Preparado para deploy en Render - Versión final"

# Push a GitHub
git push origin main
```

---

### ✅ 3.4 Verificar en GitHub

- [ ] ✅ El código está en GitHub
- [ ] ✅ Todos los archivos necesarios están ahí
- [ ] ✅ Los archivos excluidos por `.gitignore` NO están ahí
- [ ] ✅ La rama `main` está actualizada

**Verificar en GitHub:**
1. Ve a tu repositorio en GitHub
2. Verifica que todos los archivos estén presentes
3. Verifica que `Procfile`, `build.sh`, `requirements.txt` estén ahí
4. Verifica que `db.sqlite3`, `venv/`, etc. NO estén ahí

---

## 📋 FASE 4: Generar SECRET_KEY

### ✅ 4.1 Generar SECRET_KEY para Producción

- [ ] ✅ Se generó una nueva SECRET_KEY única
- [ ] ✅ La SECRET_KEY está guardada en un lugar seguro
- [ ] ✅ NO está hardcodeada en el código

**Comando:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**⚠️ IMPORTANTE:**
- Guarda esta clave en un lugar seguro
- La necesitarás para configurar la variable de entorno en Render
- NO la compartas públicamente
- NO la subas a GitHub

**Ejemplo de salida:**
```
django-insecure-abc123xyz789def456ghi012jkl345mno678pqr901stu234vwx567yz
```

---

## 📋 FASE 5: Preparación para Render

### ✅ 5.1 Crear Cuenta en Render

- [ ] ✅ Tienes cuenta en Render.com
- [ ] ✅ Conectaste tu cuenta de GitHub a Render
- [ ] ✅ Tienes acceso al dashboard de Render

**Pasos:**
1. Ve a https://render.com
2. Crea una cuenta o inicia sesión
3. Conecta tu cuenta de GitHub
4. Autoriza el acceso a tus repositorios

---

### ✅ 5.2 Preparar Información Necesaria

Antes de crear los servicios en Render, prepara:

- [ ] ✅ SECRET_KEY generada (guardada en lugar seguro)
- [ ] ✅ Nombre para la base de datos (ej: `cadmium-db`)
- [ ] ✅ Nombre para el web service (ej: `cadmium`)
- [ ] ✅ Región preferida (ej: `Oregon (US West)` o `Frankfurt (EU Central)`)
- [ ] ✅ Plan (Free para empezar)

---

## 📋 FASE 6: Checklist de Archivos del Proyecto

### ✅ 6.1 Estructura de Archivos

Verifica que la estructura del proyecto esté correcta:

```
Cadmium/
├── Procfile ✅
├── build.sh ✅
├── requirements.txt ✅
├── runtime.txt ✅
├── .gitignore ✅
├── manage.py ✅
├── cadmium/
│   ├── __init__.py ✅
│   ├── settings.py ✅
│   ├── urls.py ✅
│   ├── wsgi.py ✅
│   └── asgi.py ✅
├── core/
│   ├── __init__.py ✅
│   ├── models.py ✅
│   ├── views.py ✅
│   ├── urls.py ✅
│   ├── admin.py ✅
│   └── migrations/ ✅
├── templates/ ✅
├── static/ ✅
└── media/ ✅ (puede estar vacío)
```

---

### ✅ 6.2 Archivos Estáticos

- [ ] ✅ La carpeta `static/` existe
- [ ] ✅ Contiene `css/`, `js/`, `images/`
- [ ] ✅ Los archivos estáticos están organizados correctamente
- [ ] ✅ No hay archivos corruptos o faltantes

---

### ✅ 6.3 Templates

- [ ] ✅ La carpeta `templates/` existe
- [ ] ✅ Los templates principales están ahí:
  - [ ] `templates/core/base.html`
  - [ ] `templates/core/index.html`
  - [ ] `templates/core/login.html`
  - [ ] Etc.
- [ ] ✅ No hay templates con errores de sintaxis

---

### ✅ 6.4 Migraciones

- [ ] ✅ La carpeta `core/migrations/` existe
- [ ] ✅ Contiene todas las migraciones necesarias
- [ ] ✅ No hay migraciones conflictivas
- [ ] ✅ La migración inicial está presente

---

## 📋 FASE 7: Verificaciones de Seguridad

### ✅ 7.1 Configuración de Seguridad

- [ ] ✅ `DEBUG` estará en `False` en producción (se configurará en Render)
- [ ] ✅ `SECRET_KEY` será única y segura (se configurará en Render)
- [ ] ✅ `ALLOWED_HOSTS` estará configurado correctamente (se configurará en Render)
- [ ] ✅ No hay credenciales hardcodeadas en el código
- [ ] ✅ No hay información sensible en el código

---

### ✅ 7.2 Variables de Entorno

- [ ] ✅ Las variables sensibles se obtienen de variables de entorno
- [ ] ✅ No hay valores por defecto inseguros en producción
- [ ] ✅ El archivo `.env` está en `.gitignore`

---

### ✅ 7.3 Admin de Django

- [ ] ✅ La URL del admin es personalizada (no `/admin/`)
- [ ] ✅ Hay middleware de seguridad configurado
- [ ] ✅ El admin tiene protección contra fuerza bruta (si está implementado)

**Verificar en `cadmium/urls.py`:**
```python
ADMIN_URL = os.environ.get('ADMIN_URL', 'admin-cadmium-secreto-2025/')
```

---

## 📋 FASE 8: Documentación

### ✅ 8.1 Documentación del Proyecto

- [ ] ✅ `README.md` está actualizado
- [ ] ✅ Contiene instrucciones de instalación
- [ ] ✅ Contiene información sobre el proyecto

---

### ✅ 8.2 Documentación de Deploy

- [ ] ✅ Tienes acceso a `INSTRUCCIONES_RENDER_PASO_A_PASO.md`
- [ ] ✅ Tienes acceso a `RESPUESTAS_DEPLOY_RENDER.md`
- [ ] ✅ Tienes acceso a `CHECKLIST_ANTES_DEPLOY_RENDER.md`

---

## 📋 FASE 9: Logo (Opcional)

### ✅ 9.1 Preparación del Logo

- [ ] ⏳ Logo preparado (puede ser después del deploy)
- [ ] ⏳ Favicon preparado (puede ser después del deploy)
- [ ] ✅ Carpeta `static/images/logo/` creada
- [ ] ✅ Sistema de fallback implementado (mostrará "C" si no hay logo)

**Nota:** El logo puede agregarse después del deploy sin problemas.

---

## 📋 FASE 10: Checklist Final Pre-Deploy

### ✅ 10.1 Verificación Final

Antes de proceder con el deploy en Render, verifica:

- [ ] ✅ Todos los archivos críticos están presentes
- [ ] ✅ El código funciona localmente
- [ ] ✅ Las migraciones están actualizadas
- [ ] ✅ Los archivos estáticos se recopilan correctamente
- [ ] ✅ El código está en GitHub
- [ ] ✅ SECRET_KEY está generada y guardada
- [ ] ✅ Tienes cuenta en Render
- [ ] ✅ GitHub está conectado a Render
- [ ] ✅ Tienes la documentación a mano

---

### ✅ 10.2 Resumen de lo que Necesitas para Render

**Información necesaria:**
1. ✅ SECRET_KEY (generada)
2. ✅ Repositorio de GitHub (conectado)
3. ✅ Nombre para la base de datos
4. ✅ Nombre para el web service
5. ✅ Región preferida

**Variables de entorno a configurar en Render:**
1. `SECRET_KEY` = (la que generaste)
2. `DEBUG` = `False`
3. `ALLOWED_HOSTS` = `tu-app.onrender.com` (Render te dará el dominio)
4. `DATABASE_URL` = (Render te dará esto al crear la BD)
5. `ADMIN_URL` = `admin-cadmium-secreto-2025/` (o algo único)

**Comandos en Render:**
- Build Command: `./build.sh`
- Start Command: `gunicorn cadmium.wsgi:application`

---

## 🚀 Siguiente Paso: Deploy en Render

Una vez completada esta checklist, estás listo para:

1. ✅ Crear la base de datos PostgreSQL en Render
2. ✅ Crear el Web Service en Render
3. ✅ Configurar las variables de entorno
4. ✅ Hacer el deploy
5. ✅ Crear el superusuario
6. ✅ Verificar que todo funciona

**📖 Para los pasos detallados, consulta: `INSTRUCCIONES_RENDER_PASO_A_PASO.md`**

---

## ✅ Estado Actual del Proyecto

### Archivos Verificados ✅

- [x] `Procfile` - ✅ Correcto
- [x] `build.sh` - ✅ Correcto
- [x] `requirements.txt` - ✅ Correcto (tiene todas las dependencias)
- [x] `runtime.txt` - ✅ Correcto (Python 3.12.7)
- [x] `.gitignore` - ✅ Correcto (excluye archivos sensibles)
- [x] `cadmium/settings.py` - ✅ Configurado para producción
- [x] `static/js/logo-loader.js` - ✅ Creado (soporte para logo)
- [x] Templates actualizados - ✅ Logo implementado con fallback

### Pendiente ⏳

- [ ] Generar SECRET_KEY (hacer antes del deploy)
- [ ] Hacer commit final y push a GitHub
- [ ] Crear cuenta en Render (si no la tienes)
- [ ] Crear base de datos PostgreSQL en Render
- [ ] Crear Web Service en Render
- [ ] Configurar variables de entorno en Render
- [ ] Hacer el deploy
- [ ] Crear superusuario
- [ ] Agregar logo (opcional, puede ser después)

---

## 🎯 Orden de Ejecución Recomendado

```
1. ✅ Verificar archivos críticos (FASE 1)
2. ✅ Probar localmente (FASE 2)
3. ✅ Preparar Git y GitHub (FASE 3)
4. ✅ Generar SECRET_KEY (FASE 4)
5. ✅ Crear cuenta en Render (FASE 5)
6. ✅ Verificar estructura del proyecto (FASE 6)
7. ✅ Verificar seguridad (FASE 7)
8. ✅ Revisar documentación (FASE 8)
9. ⏳ Logo (opcional, puede ser después)
10. ✅ Checklist final (FASE 10)
11. 🚀 Deploy en Render
```

---

## 📞 ¿Necesitas Ayuda?

- **Guía paso a paso**: `INSTRUCCIONES_RENDER_PASO_A_PASO.md`
- **Respuestas a preguntas**: `RESPUESTAS_DEPLOY_RENDER.md`
- **Resumen ejecutivo**: `DEPLOY_RENDER_RESUMEN.md`
- **Checklist detallada**: `CHECKLIST_ANTES_DEPLOY_RENDER.md`

---

## 🎉 ¡Listo para el Deploy!

Una vez completada esta checklist, estás completamente preparado para hacer el deploy en Render.

**¡Buena suerte con el deploy!** 🚀

