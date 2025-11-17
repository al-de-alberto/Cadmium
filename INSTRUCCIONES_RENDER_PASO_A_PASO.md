# 📋 Instrucciones Paso a Paso: Deploy en Render

## 🎯 Paso 1: Preparación Local

### 1.1 Generar SECRET_KEY

Abre PowerShell o Terminal y ejecuta:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Copia y guarda esta clave** - La necesitarás en el Paso 4.

**Ejemplo de salida:**
```
django-insecure-abc123xyz789def456ghi012jkl345mno678pqr901stu234vwx567yz
```

---

### 1.2 Hacer Commit Final

```bash
# Verificar estado
git status

# Agregar todos los cambios
git add .

# Hacer commit
git commit -m "Preparado para deploy en Render - Versión final"

# Subir a GitHub
git push origin main
```

**Verifica en GitHub** que todos los archivos estén subidos (excepto los que están en `.gitignore`).

---

## 🎯 Paso 2: Crear Cuenta en Render

1. Ve a: https://render.com
2. Click en **"Get Started for Free"**
3. Selecciona **"Sign up with GitHub"**
4. Autoriza la conexión con GitHub
5. Completa el registro si es necesario

---

## 🎯 Paso 3: Crear Base de Datos PostgreSQL

1. En el Dashboard de Render, click en **"New +"** → **"PostgreSQL"**

2. Configuración:
   - **Name**: `cadmium-db` (o el nombre que prefieras)
   - **Database**: `cadmium_db`
   - **User**: Se genera automáticamente
   - **Region**: Elige la más cercana (ej: `Oregon (US West)` o `Frankfurt (EU Central)`)
   - **PostgreSQL Version**: `15` (o la más reciente disponible)
   - **Plan**: `Free` (para empezar)

3. Click en **"Create Database"**

4. **⚠️ IMPORTANTE:** Espera a que la base de datos se cree (1-2 minutos)

5. Una vez creada, ve a la pestaña **"Info"** y copia:
   - **Internal Database URL** (formato: `postgresql://user:password@host:port/dbname`)
   
   **Guarda esta URL** - La necesitarás en el siguiente paso.

---

## 🎯 Paso 4: Crear Web Service

1. En el Dashboard de Render, click en **"New +"** → **"Web Service"**

2. **Conectar Repositorio:**
   - Selecciona **"Connect GitHub"** (si no lo has hecho)
   - Autoriza si es necesario
   - Selecciona tu repositorio `Cadmium` (o el nombre que tenga)

3. **Configuración del Servicio:**
   - **Name**: `cadmium` (o el nombre que prefieras)
   - **Region**: **La misma que la base de datos** (muy importante)
   - **Branch**: `main` (o la rama que uses)
   - **Root Directory**: (dejar vacío)
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn cadmium.wsgi:application`

4. **⚠️ NO hacer click en "Create Web Service" todavía**

---

## 🎯 Paso 5: Configurar Variables de Entorno

Antes de crear el servicio, configura estas variables en la sección **"Environment Variables"**:

### Variable 1: SECRET_KEY
- **Key**: `SECRET_KEY`
- **Value**: La clave que generaste en el Paso 1.1
- Click en **"Add"**

### Variable 2: DEBUG
- **Key**: `DEBUG`
- **Value**: `False`
- Click en **"Add"**
- ⚠️ **MUY IMPORTANTE:** Debe ser `False` en producción

### Variable 3: ALLOWED_HOSTS
- **Key**: `ALLOWED_HOSTS`
- **Value**: `cadmium.onrender.com` (o el dominio que Render te asigne)
- **Nota:** Render te dará el dominio exacto después de crear el servicio. Puedes actualizarlo después.
- Click en **"Add"**

### Variable 4: DATABASE_URL
- **Key**: `DATABASE_URL`
- **Value**: La "Internal Database URL" que copiaste en el Paso 3
- Click en **"Add"**

**✅ Verifica que tengas estas 4 variables configuradas antes de continuar.**

---

## 🎯 Paso 6: Crear el Servicio

1. Después de configurar las variables de entorno
2. Scroll hacia abajo
3. Click en **"Create Web Service"**
4. Render iniciará el proceso de build
5. **Espera 3-5 minutos** mientras se construye

---

## 🎯 Paso 7: Verificar el Build

1. Ve a la sección **"Logs"** en Render
2. Observa el proceso de build
3. Busca mensajes como:
   - ✅ "Installing dependencies"
   - ✅ "Collecting static files"
   - ✅ "Running migrations"
   - ✅ "Build successful"
   - ✅ "Starting service"
   - ✅ "Listening on port XXXX"

**Si hay errores:**
- Revisa los logs detalladamente
- Verifica las variables de entorno
- Verifica que `build.sh` tenga el contenido correcto

---

## 🎯 Paso 8: Actualizar ALLOWED_HOSTS

1. Una vez que el servicio esté corriendo, Render te dará un dominio
2. Ve a tu servicio en Render
3. Click en **"Environment"** (en el menú lateral)
4. Busca la variable `ALLOWED_HOSTS`
5. Click en el ícono de editar (lápiz)
6. Actualiza el valor con el dominio real que Render te dio
   - Ejemplo: `cadmium-xxxx.onrender.com`
7. Click en **"Save Changes"**
8. Render redesplegará automáticamente (espera 1-2 minutos)

---

## 🎯 Paso 9: Crear Superusuario

1. Ve a tu servicio en Render
2. Click en **"Shell"** (en el menú lateral)
3. Se abrirá una terminal en el navegador
4. Ejecuta:
   ```bash
   python manage.py createsuperuser
   ```
5. Sigue las instrucciones:
   - **Username**: `Gerencia` (o el que prefieras)
   - **Email**: (opcional, presiona Enter)
   - **Password**: Ingresa una contraseña segura
   - **Password (again)**: Confirma la contraseña

**O si tienes un comando personalizado:**
```bash
python manage.py create_gerencia
```

---

## 🎯 Paso 10: Verificar que Todo Funciona

1. Abre tu aplicación en el navegador:
   - URL: `https://tu-dominio.onrender.com/`
   - (Render te dará el dominio exacto)

2. Verifica:
   - [ ] ✅ La página principal carga
   - [ ] ✅ Puedes hacer login
   - [ ] ✅ El admin funciona: `https://tu-dominio.onrender.com/admin-cadmium-secreto-2025/`
   - [ ] ✅ Los archivos estáticos se cargan (CSS, imágenes)
   - [ ] ✅ La base de datos funciona (puedes crear/editar datos)

---

## 🎯 Paso 11: Subir Logo (Cuando Esté Listo)

1. Accede al admin: `https://tu-dominio.onrender.com/admin-cadmium-secreto-2025/`
2. Inicia sesión con el usuario que creaste
3. Ve a la sección donde se gestiona el logo
4. Sube el logo desde ahí
5. Los cambios se guardarán automáticamente

---

## 🚨 Solución de Problemas

### Error: "ModuleNotFoundError"
- Verifica que todas las dependencias estén en `requirements.txt`
- Revisa los logs para ver qué módulo falta

### Error: "Database connection failed"
- Verifica que `DATABASE_URL` esté correcta
- Verifica que la base de datos esté en la misma región
- Verifica que la base de datos esté activa (no en sleep mode)

### Error: "Static files not found"
- Verifica que `collectstatic` esté en `build.sh` ✅ (ya está)
- Verifica que WhiteNoise esté en `requirements.txt` ✅ (ya está)

### Error: "502 Bad Gateway"
- Revisa los logs en Render
- Verifica que `Procfile` sea correcto ✅ (ya está)
- Verifica que `gunicorn` esté en `requirements.txt` ✅ (ya está)

### El servicio está en "Sleep Mode"
- Es normal en el plan gratuito después de 15 minutos de inactividad
- Se despierta automáticamente cuando alguien lo visita (puede tardar 30-60 segundos)
- Para evitar sleep mode, considera el plan de pago

---

## ✅ Checklist Final

- [ ] SECRET_KEY generada y guardada
- [ ] Commit final hecho y subido a GitHub
- [ ] Cuenta de Render creada
- [ ] Base de datos PostgreSQL creada
- [ ] Variables de entorno configuradas
- [ ] Web Service creado
- [ ] Build exitoso
- [ ] ALLOWED_HOSTS actualizado
- [ ] Superusuario creado
- [ ] Aplicación funciona correctamente

---

## 🎉 ¡Listo!

Tu aplicación está desplegada y funcionando. Cada vez que hagas `git push` a la rama que Render está monitoreando, se hará un redeploy automático.

**Para más detalles, consulta:**
- `RESPUESTAS_DEPLOY_RENDER.md` - Respuestas completas a tus preguntas
- `DEPLOY_RENDER_RESUMEN.md` - Resumen ejecutivo
- `CHECKLIST_ANTES_DEPLOY_RENDER.md` - Checklist detallada

---

**¡Felicitaciones por el deploy!** 🚀













