# ✅ Checklist: Antes de Hacer Deploy en Render

## 🎯 Preparación Completa Paso a Paso

---

## 📋 FASE 1: Preparación del Código

### ✅ 1.1 Verificar Archivos Críticos

Verifica que estos archivos existan y estén correctos:

- [ ] `Procfile` - Existe y tiene el contenido correcto
- [ ] `build.sh` - Existe y tiene permisos de ejecución
- [ ] `requirements.txt` - Tiene todas las dependencias
- [ ] `cadmium/settings.py` - Configurado para producción
- [ ] `.gitignore` - Excluye archivos sensibles

**Verificar:**
```bash
# Verificar que los archivos existen
ls -la Procfile build.sh requirements.txt

# Ver contenido de Procfile
cat Procfile
# Debe decir: web: gunicorn cadmium.wsgi:application

# Ver contenido de build.sh
cat build.sh
```

---

### ✅ 1.2 Probar Localmente

Antes de desplegar, prueba que todo funcione:

- [ ] El servidor inicia sin errores
- [ ] Las migraciones se aplican correctamente
- [ ] Los archivos estáticos se recopilan
- [ ] La aplicación funciona en desarrollo

**Comandos de prueba:**
```bash
# 1. Probar que el servidor inicia
python manage.py runserver
# Debe iniciar sin errores

# 2. Verificar que no hay errores
python manage.py check
# Debe decir: "System check identified no issues"

# 3. Probar migraciones
python manage.py makemigrations
python manage.py migrate
# Debe aplicar sin errores

# 4. Probar collectstatic
python manage.py collectstatic --dry-run
# Debe mostrar los archivos que se recopilarían
```

---

### ✅ 1.3 Verificar Configuración de Base de Datos

- [ ] `settings.py` está configurado para usar PostgreSQL en producción
- [ ] SQLite funciona en desarrollo
- [ ] Las migraciones están actualizadas

**Verificar en `cadmium/settings.py`:**
```python
# Debe tener lógica para PostgreSQL en producción
if os.environ.get('DATABASE_URL'):
    # Usar PostgreSQL
elif os.environ.get('DATABASE_NAME'):
    # Usar PostgreSQL con variables individuales
else:
    # Usar SQLite (desarrollo)
```

---

### ✅ 1.4 Crear Usuario Administrador (Opcional pero Recomendado)

Tienes dos opciones:

**Opción A: Crear superusuario después del deploy (Recomendado)**
- Más seguro
- Lo harás desde Render Shell después del deploy

**Opción B: Usar el comando existente**
```bash
python manage.py create_gerencia
```

**Recomendación:** Crear el superusuario después del deploy desde Render Shell.

---

## 📋 FASE 2: Preparación de GitHub

### ✅ 2.1 Verificar que el Código está en GitHub

- [ ] Tienes una cuenta de GitHub
- [ ] Tienes un repositorio creado
- [ ] El código está subido a GitHub

**Si NO tienes el código en GitHub:**

```bash
# 1. Inicializar Git (si no está inicializado)
git init

# 2. Agregar todos los archivos
git add .

# 3. Hacer commit inicial
git commit -m "Preparado para producción - Cadmium"

# 4. Crear repositorio en GitHub (desde el navegador)
# Ve a: https://github.com/new
# Crea un repositorio (por ejemplo: "cadmium")

# 5. Conectar y subir
git remote add origin https://github.com/TU-USUARIO/cadmium.git
git branch -M main
git push -u origin main
```

**Si YA tienes el código en GitHub:**

```bash
# Verificar que esté actualizado
git status
git add .
git commit -m "Preparado para deploy en Render"
git push origin main
```

---

### ✅ 2.2 Verificar .gitignore

Asegúrate de que `.gitignore` excluya:

- [ ] `db.sqlite3` (base de datos local)
- [ ] `venv/` (entorno virtual)
- [ ] `__pycache__/` (archivos Python compilados)
- [ ] `*.log` (archivos de log)
- [ ] `.env` (variables de entorno locales)
- [ ] `staticfiles/` (archivos estáticos compilados)
- [ ] `media/` (archivos subidos por usuarios)

**Verificar:**
```bash
cat .gitignore
```

---

## 📋 FASE 3: Preparación de Render

### ✅ 3.1 Crear Cuenta en Render

- [ ] Tienes cuenta en Render.com
- [ ] Conectaste tu cuenta de GitHub a Render

**Si NO tienes cuenta:**

1. Ve a: https://render.com
2. Click en "Get Started for Free"
3. Selecciona "Sign up with GitHub"
4. Autoriza la conexión

---

### ✅ 3.2 Generar Secret Key

Necesitas una clave secreta única para producción:

- [ ] Generaste una nueva SECRET_KEY

**Generar SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Guarda esta clave** - La necesitarás para las variables de entorno.

**Ejemplo de salida:**
```
django-insecure-abc123xyz789... (muy larga)
```

---

## 📋 FASE 4: Crear Servicios en Render

### ✅ 4.1 Crear Base de Datos PostgreSQL

**Pasos:**

1. En Render Dashboard, click en "New +" → "PostgreSQL"

2. Configuración:
   - **Name**: `cadmium-db` (o el nombre que prefieras)
   - **Database**: `cadmium_db`
   - **User**: Se genera automáticamente
   - **Region**: Elige la más cercana (ej: `Oregon (US West)`)
   - **PostgreSQL Version**: `15` (o la más reciente)
   - **Plan**: `Free` (para empezar)

3. Click en "Create Database"

4. **IMPORTANTE:** Anota las credenciales que Render te da:
   - **Host**: `dpg-xxxxx-a.oregon-postgres.render.com`
   - **Database Name**: `cadmium_db`
   - **User**: `cadmium_db_user`
   - **Password**: `xxxxx` (generada automáticamente)
   - **Port**: `5432`
   - **Internal Database URL**: `postgresql://user:password@host:port/dbname`

**⚠️ Guarda estas credenciales - Las necesitarás después.**

---

### ✅ 4.2 Crear Web Service

**Pasos:**

1. En Render Dashboard, click en "New +" → "Web Service"

2. Conecta tu repositorio:
   - Selecciona "Connect GitHub"
   - Autoriza si es necesario
   - Selecciona tu repositorio `cadmium`

3. Configuración del servicio:
   - **Name**: `cadmium` (o el nombre que prefieras)
   - **Region**: La misma que la base de datos
   - **Branch**: `main`
   - **Root Directory**: (dejar vacío)
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn cadmium.wsgi:application`

4. **NO hacer click en "Create Web Service" todavía** - Primero configuraremos las variables de entorno.

---

### ✅ 4.3 Configurar Variables de Entorno

**ANTES de crear el servicio**, configura estas variables:

**Variables necesarias:**

1. **SECRET_KEY**
   - Valor: La clave que generaste antes
   - Ejemplo: `django-insecure-abc123xyz789...`

2. **DEBUG**
   - Valor: `False`
   - ⚠️ **MUY IMPORTANTE:** Debe ser `False` en producción

3. **ALLOWED_HOSTS**
   - Valor: `cadmium.onrender.com` (o el dominio que Render te asigne)
   - Nota: Render te dirá el dominio después de crear el servicio
   - Puedes actualizarlo después

4. **ADMIN_URL**
   - Valor: `admin-cadmium-secreto-2025/` (o algo único)
   - ⚠️ **IMPORTANTE:** Cámbialo a algo único y secreto

5. **DATABASE_URL** (Opción A - Más fácil)
   - Valor: La "Internal Database URL" que Render te dio
   - Formato: `postgresql://user:password@host:port/dbname`

   **O** variables individuales (Opción B):

6. **DATABASE_NAME**
   - Valor: `cadmium_db`

7. **DATABASE_USER**
   - Valor: El usuario que Render generó

8. **DATABASE_PASSWORD**
   - Valor: La contraseña que Render generó

9. **DATABASE_HOST**
   - Valor: El host que Render te dio
   - Ejemplo: `dpg-xxxxx-a.oregon-postgres.render.com`

10. **DATABASE_PORT**
    - Valor: `5432`

**⚠️ Recomendación:** Usa `DATABASE_URL` (Opción A) - Es más simple.

---

## 📋 FASE 5: Crear el Servicio

### ✅ 5.1 Crear Web Service

1. Después de configurar las variables de entorno
2. Click en "Create Web Service"
3. Render iniciará el proceso de build
4. Espera 3-5 minutos

---

### ✅ 5.2 Verificar el Build

1. Ve a la sección "Logs" en Render
2. Verifica que no haya errores
3. Busca mensajes como:
   - ✅ "Build successful"
   - ✅ "Starting service"
   - ✅ "Listening on port XXXX"

**Si hay errores:**
- Revisa los logs
- Verifica las variables de entorno
- Verifica que `build.sh` tenga permisos de ejecución

---

## 📋 FASE 6: Configuración Post-Deploy

### ✅ 6.1 Actualizar ALLOWED_HOSTS

Después de que Render asigne el dominio:

1. Ve a tu servicio en Render
2. Click en "Environment"
3. Actualiza `ALLOWED_HOSTS` con el dominio real
4. Ejemplo: `cadmium-xxxx.onrender.com`
5. Render redesplegará automáticamente

---

### ✅ 6.2 Crear Superusuario

1. Ve a tu servicio en Render
2. Click en "Shell" (en el menú lateral)
3. Ejecuta:
```bash
python manage.py createsuperuser
```
4. Sigue las instrucciones:
   - Username: `Gerencia` (o el que prefieras)
   - Email: (opcional)
   - Password: `Ger_2O25` (o una contraseña segura)

**⚠️ IMPORTANTE:** Usa una contraseña segura en producción.

---

### ✅ 6.3 Cargar Datos Iniciales (Si es necesario)

Si tienes comandos de management personalizados:

1. Ve a "Shell" en Render
2. Ejecuta tus comandos:
```bash
python manage.py create_gerencia
python manage.py init_inventario
# etc.
```

---

### ✅ 6.4 Verificar que Todo Funciona

1. Abre tu aplicación en el navegador:
   - URL: `https://cadmium-xxxx.onrender.com/`
2. Verifica:
   - ✅ La página principal carga
   - ✅ Puedes hacer login
   - ✅ El admin funciona: `https://cadmium-xxxx.onrender.com/admin-cadmium-secreto-2025/`
   - ✅ Los archivos estáticos se cargan (CSS, imágenes)
   - ✅ La base de datos funciona (puedes crear/editar datos)

---

## 📋 FASE 7: Verificaciones Finales

### ✅ 7.1 Seguridad

- [ ] `DEBUG=False` en producción
- [ ] `SECRET_KEY` es única y segura
- [ ] `ADMIN_URL` es única y secreta
- [ ] `ALLOWED_HOSTS` está configurado correctamente
- [ ] HTTPS está activo (automático en Render)

---

### ✅ 7.2 Funcionalidad

- [ ] La aplicación carga correctamente
- [ ] El login funciona
- [ ] El admin es accesible
- [ ] Los archivos estáticos se cargan
- [ ] La base de datos funciona
- [ ] Puedes crear/editar datos

---

### ✅ 7.3 Logs

- [ ] Revisa los logs en Render
- [ ] No hay errores críticos
- [ ] Los logs de seguridad se generan (si los configuraste)

---

## 🚨 Problemas Comunes y Soluciones

### ❌ Error: "ModuleNotFoundError: No module named 'whitenoise'"

**Solución:**
- Verifica que `whitenoise>=6.6.0` esté en `requirements.txt`
- Render lo instalará automáticamente

---

### ❌ Error: "Command './build.sh' failed"

**Solución:**
1. Verifica que `build.sh` exista
2. Verifica que tenga el contenido correcto:
```bash
#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

---

### ❌ Error: "Database connection failed"

**Solución:**
1. Verifica las variables de entorno de la base de datos
2. Asegúrate de usar `DATABASE_URL` o todas las variables individuales
3. Verifica que la base de datos esté creada en Render
4. Verifica que la base de datos esté en la misma región

---

### ❌ Error: "Static files not found"

**Solución:**
1. Verifica que `collectstatic` esté en `build.sh`
2. Verifica la configuración de WhiteNoise en `settings.py`
3. Verifica que `STATIC_ROOT` esté configurado

---

### ❌ Error: "502 Bad Gateway"

**Solución:**
1. Verifica que `Procfile` sea correcto
2. Verifica que `gunicorn` esté en `requirements.txt`
3. Revisa los logs en Render para más detalles

---

## 📊 Resumen: Checklist Rápida

### **Antes del Deploy:**
- [ ] Código probado localmente
- [ ] Archivos críticos verificados (Procfile, build.sh, requirements.txt)
- [ ] Código subido a GitHub
- [ ] Cuenta de Render creada
- [ ] SECRET_KEY generada

### **En Render:**
- [ ] Base de datos PostgreSQL creada
- [ ] Variables de entorno configuradas
- [ ] Web Service creado
- [ ] Build exitoso

### **Después del Deploy:**
- [ ] Superusuario creado
- [ ] ALLOWED_HOSTS actualizado
- [ ] Aplicación funciona correctamente
- [ ] Admin es accesible
- [ ] Logs revisados

---

## 🎯 Orden de Ejecución

```
1. Preparar código localmente ✅
2. Probar localmente ✅
3. Subir a GitHub ✅
4. Crear cuenta en Render ✅
5. Generar SECRET_KEY ✅
6. Crear base de datos PostgreSQL ✅
7. Crear Web Service ✅
8. Configurar variables de entorno ✅
9. Crear servicio ✅
10. Esperar build (3-5 minutos) ✅
11. Crear superusuario ✅
12. Verificar que todo funciona ✅
```

---

## ✅ Listo para Deploy

Una vez completada esta checklist, estás listo para hacer el deploy.

**¿Necesitas ayuda con algún paso?** Consulta la guía detallada en `GUIA_DESPLIEGUE_RENDER.md`

---

**¡Buena suerte con el deploy!** 🚀














