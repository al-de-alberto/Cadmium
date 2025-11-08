# 🔍 Repaso Completo: Todo lo Necesario Antes del Deploy

## 📋 Índice

1. [Verificación de Archivos Críticos](#1-verificación-de-archivos-críticos)
2. [Pruebas Locales](#2-pruebas-locales)
3. [Preparación de Git y GitHub](#3-preparación-de-git-y-github)
4. [Generar SECRET_KEY](#4-generar-secret_key)
5. [Preparación para Render](#5-preparación-para-render)
6. [Checklist Final](#6-checklist-final)

---

## 1. Verificación de Archivos Críticos

### ✅ Archivos que DEBEN existir

| Archivo | Estado | Verificación |
|---------|--------|--------------|
| `Procfile` | ✅ | Debe contener: `web: gunicorn cadmium.wsgi:application` |
| `build.sh` | ✅ | Debe tener: `pip install`, `collectstatic`, `migrate` |
| `requirements.txt` | ✅ | Debe tener todas las dependencias |
| `runtime.txt` | ✅ | Debe tener: `python-3.12.7` |
| `.gitignore` | ✅ | Debe excluir: `db.sqlite3`, `venv/`, `.env`, etc. |
| `cadmium/settings.py` | ✅ | Debe estar configurado para producción |

### 🔍 Verificar Archivos

```powershell
# Verificar que existen
Test-Path Procfile
Test-Path build.sh
Test-Path requirements.txt
Test-Path runtime.txt
Test-Path .gitignore

# Ver contenido
Get-Content Procfile
Get-Content build.sh
Get-Content requirements.txt
```

### ✅ Contenido Esperado

**Procfile:**
```
web: gunicorn cadmium.wsgi:application
```

**build.sh:**
```bash
#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

**requirements.txt:**
```
Django==4.2.7
psycopg2-binary>=2.9.9
Pillow>=10.3.0
openpyxl>=3.1.2
whitenoise>=6.6.0
gunicorn>=21.2.0
dj-database-url>=2.1.0
```

---

## 2. Pruebas Locales

### ✅ Pruebas que DEBES hacer

| Prueba | Comando | Resultado Esperado |
|--------|---------|-------------------|
| Django Check | `python manage.py check` | "System check identified no issues" |
| Migraciones | `python manage.py makemigrations --check --dry-run` | Sin migraciones pendientes |
| Aplicar Migraciones | `python manage.py migrate` | "Applying migrations... OK" |
| Collect Static | `python manage.py collectstatic --dry-run` | Lista de archivos a recopilar |
| Servidor | `python manage.py runserver` | Servidor inicia sin errores |

### 🔍 Ejecutar Pruebas

```powershell
# 1. Verificar que no hay errores
python manage.py check

# 2. Verificar migraciones
python manage.py makemigrations --check --dry-run

# 3. Aplicar migraciones (si es necesario)
python manage.py migrate

# 4. Verificar archivos estáticos
python manage.py collectstatic --dry-run

# 5. Probar servidor (opcional)
python manage.py runserver
# Presiona Ctrl+C para detener
```

---

## 3. Preparación de Git y GitHub

### ✅ Verificaciones de Git

| Verificación | Comando | Resultado Esperado |
|--------------|---------|-------------------|
| Estado de Git | `git status` | Muestra archivos modificados |
| Remoto configurado | `git remote -v` | Muestra tu repositorio de GitHub |
| Archivos a commitear | `git status` | NO debe incluir: `db.sqlite3`, `venv/`, `.env` |

### 🔍 Verificar Git

```powershell
# Verificar estado
git status

# Verificar remoto
git remote -v

# Verificar qué se va a commitear
git status
```

### ✅ Hacer Commit Final

```powershell
# 1. Agregar todos los cambios
git add .

# 2. Verificar qué se va a commitear
git status

# 3. Hacer commit
git commit -m "Preparado para deploy en Render - Versión final"

# 4. Push a GitHub
git push origin main
```

### ⚠️ Verificar que NO se suban archivos sensibles

**NO deben estar en el commit:**
- ❌ `db.sqlite3`
- ❌ `venv/` o `env/`
- ❌ `.env`
- ❌ `staticfiles/`
- ❌ `__pycache__/`
- ❌ `*.log`

**SÍ deben estar en el commit:**
- ✅ `Procfile`
- ✅ `build.sh`
- ✅ `requirements.txt`
- ✅ `runtime.txt`
- ✅ `.gitignore`
- ✅ Todo el código fuente
- ✅ Templates
- ✅ Archivos estáticos (static/)

---

## 4. Generar SECRET_KEY

### ✅ Generar SECRET_KEY

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### ⚠️ IMPORTANTE

1. **Guarda la clave** en un lugar seguro
2. **NO la subas a GitHub**
3. **La necesitarás** para configurar en Render
4. **Debe ser única** para producción

### 📝 Ejemplo de salida

```
django-insecure-abc123xyz789def456ghi012jkl345mno678pqr901stu234vwx567yz
```

---

## 5. Preparación para Render

### ✅ Cuenta en Render

- [ ] Tienes cuenta en Render.com
- [ ] Conectaste tu cuenta de GitHub a Render
- [ ] Tienes acceso al dashboard de Render

**Si NO tienes cuenta:**
1. Ve a https://render.com
2. Click en "Get Started for Free"
3. Selecciona "Sign up with GitHub"
4. Autoriza la conexión

### ✅ Información Necesaria

**Antes de crear los servicios, prepara:**

1. **SECRET_KEY** - Ya generada (paso 4)
2. **Nombre para la base de datos** - Ej: `cadmium-db`
3. **Nombre para el web service** - Ej: `cadmium`
4. **Región** - Ej: `Oregon (US West)` o `Frankfurt (EU Central)`
5. **Plan** - `Free` (para empezar)

### ✅ Variables de Entorno a Configurar en Render

| Variable | Valor | Notas |
|----------|-------|-------|
| `SECRET_KEY` | (la que generaste) | Clave única para producción |
| `DEBUG` | `False` | ⚠️ MUY IMPORTANTE: Debe ser False |
| `ALLOWED_HOSTS` | `tu-app.onrender.com` | Render te dará el dominio exacto |
| `DATABASE_URL` | (Render te dará esto) | Internal Database URL de Render |
| `ADMIN_URL` | `admin-cadmium-secreto-2025/` | Opcional, ya está en el código |

### ✅ Comandos en Render

| Comando | Valor |
|---------|-------|
| **Build Command** | `./build.sh` |
| **Start Command** | `gunicorn cadmium.wsgi:application` |

---

## 6. Checklist Final

### 🔴 Crítico (Debe estar 100% completo)

- [ ] **Archivos de configuración**:
  - [ ] `Procfile` existe y es correcto
  - [ ] `build.sh` existe y es correcto
  - [ ] `requirements.txt` tiene todas las dependencias
  - [ ] `runtime.txt` especifica Python 3.12.7
  - [ ] `.gitignore` excluye archivos sensibles

- [ ] **Código funciona localmente**:
  - [ ] Servidor inicia sin errores
  - [ ] Django check no muestra errores
  - [ ] Migraciones aplicadas
  - [ ] Archivos estáticos se recopilan

- [ ] **Git y GitHub**:
  - [ ] Código en GitHub
  - [ ] Último commit hecho
  - [ ] Archivos sensibles NO están en GitHub

- [ ] **SECRET_KEY**:
  - [ ] Generada
  - [ ] Guardada en lugar seguro
  - [ ] Lista para usar en Render

- [ ] **Cuenta Render**:
  - [ ] Cuenta creada
  - [ ] GitHub conectado

---

### 🟡 Importante (Recomendado)

- [ ] **Configuración Django**:
  - [ ] `settings.py` configurado para producción
  - [ ] Variables de entorno configuradas
  - [ ] Base de datos configurada para PostgreSQL

- [ ] **Seguridad**:
  - [ ] No hay credenciales hardcodeadas
  - [ ] Admin URL personalizada
  - [ ] DEBUG será False en producción

---

### 🟢 Opcional (Puede hacerse después)

- [ ] **Logo**:
  - [ ] Logo preparado (puede agregarse después del deploy)
  - [ ] Favicon preparado (puede agregarse después del deploy)

---

## 📊 Estado Actual del Proyecto

### ✅ Verificado

- [x] `Procfile` - ✅ Correcto
- [x] `build.sh` - ✅ Correcto
- [x] `requirements.txt` - ✅ Correcto
- [x] `runtime.txt` - ✅ Correcto
- [x] `.gitignore` - ✅ Correcto
- [x] `cadmium/settings.py` - ✅ Configurado para producción
- [x] Logo sistema implementado - ✅ Con fallback

### ⏳ Pendiente

- [ ] Generar SECRET_KEY
- [ ] Hacer commit final
- [ ] Push a GitHub
- [ ] Crear cuenta en Render (si no la tienes)
- [ ] Deploy en Render

---

## 🚀 Orden de Ejecución

```
1. ✅ Verificar archivos críticos
   └── Procfile, build.sh, requirements.txt, runtime.txt, .gitignore

2. ✅ Probar localmente
   └── python manage.py check
   └── python manage.py migrate
   └── python manage.py collectstatic --dry-run

3. ✅ Generar SECRET_KEY
   └── python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

4. ✅ Hacer commit y push
   └── git add .
   └── git commit -m "Preparado para deploy en Render"
   └── git push origin main

5. ✅ Verificar en GitHub
   └── Verificar que todos los archivos estén ahí
   └── Verificar que archivos sensibles NO estén ahí

6. 🚀 Deploy en Render
   └── Crear base de datos PostgreSQL
   └── Crear Web Service
   └── Configurar variables de entorno
   └── Hacer el deploy
```

---

## 📚 Documentación Disponible

### Para Verificación Pre-Deploy

1. **`CHECKLIST_COMPLETO_PRE_DEPLOY.md`** ⭐
   - Checklist exhaustivo y detallado
   - **Úsalo para verificación completa**

2. **`RESUMEN_EJECUTIVO_PRE_DEPLOY.md`**
   - Resumen ejecutivo rápido
   - Checklist rápida

3. **`REPASO_COMPLETO_PRE_DEPLOY.md`** (este archivo)
   - Repaso completo con tablas y ejemplos
   - **Úsalo como referencia**

### Para el Deploy en Render

4. **`INSTRUCCIONES_RENDER_PASO_A_PASO.md`** ⭐
   - Guía paso a paso para el deploy
   - **Úsalo cuando hagas el deploy**

5. **`RESPUESTAS_DEPLOY_RENDER.md`**
   - Respuestas a preguntas comunes
   - Explicaciones detalladas

6. **`DEPLOY_RENDER_RESUMEN.md`**
   - Resumen ejecutivo del deploy
   - Para referencia rápida

---

## 🎯 Siguiente Paso

Una vez completada esta checklist, estás listo para:

**📖 Consultar: `INSTRUCCIONES_RENDER_PASO_A_PASO.md`** para la guía completa del deploy en Render.

---

## 🚨 Problemas Comunes

### Error: "ModuleNotFoundError"
**Solución:** Verifica que todas las dependencias estén en `requirements.txt`

### Error: "Database connection failed"
**Solución:** Verifica las variables de entorno de la base de datos en Render

### Error: "Static files not found"
**Solución:** Verifica que `collectstatic` esté en `build.sh`

### Error: "502 Bad Gateway"
**Solución:** Verifica que `Procfile` y `gunicorn` estén correctos

---

## ✅ Resumen Rápido

### Lo que DEBES hacer ahora:

1. ✅ Verificar archivos críticos (5 min)
2. ✅ Probar localmente (10 min)
3. ✅ Generar SECRET_KEY (1 min)
4. ✅ Hacer commit y push (5 min)
5. ✅ Verificar en GitHub (2 min)
6. 🚀 Deploy en Render (ver instrucciones)

**Tiempo estimado total: ~25 minutos**

---

## 🎉 ¡Listo para el Deploy!

Una vez completados todos los pasos de esta checklist, estás completamente preparado para hacer el deploy en Render.

**¡Buena suerte con el deploy!** 🚀

