# 📸 Guía: Imágenes y Datos en Producción

## ⚠️ Problema: Archivos Media en Render Free

**Render Free tiene un sistema de archivos efímero:**
- Las imágenes subidas a través del panel **se pierden** cuando el servicio se reinicia
- Los archivos en la carpeta `media/` **no persisten**
- Solo los archivos estáticos (en `static/`) se mantienen

**¿Qué significa esto?**
- Si subes imágenes de productos desde el panel, se borrarán
- Las imágenes del carrusel, eventos, noticias también se perderán
- Solo los datos en la base de datos (nombres, precios, etc.) se mantienen

---

## ✅ Soluciones Disponibles

### Opción 1: Cloudinary (Recomendado) ⭐

**Ventajas:**
- ✅ Gratis hasta 25 GB de almacenamiento
- ✅ CDN incluido (imágenes cargan rápido)
- ✅ Transformaciones de imágenes automáticas
- ✅ Fácil de configurar
- ✅ Las imágenes se almacenan permanentemente

**Desventajas:**
- ⚠️ Requiere crear una cuenta gratis
- ⚠️ Requiere instalar una librería adicional

**¿Cómo funciona?**
- Las imágenes se suben directamente a Cloudinary
- Se almacenan en la nube permanentemente
- Se acceden mediante URLs

---

### Opción 2: Imágenes como Archivos Estáticos

**Ventajas:**
- ✅ No requiere servicios externos
- ✅ Las imágenes están en el repositorio
- ✅ Funciona perfectamente en Render

**Desventajas:**
- ⚠️ Las imágenes no se pueden cambiar desde el panel
- ⚠️ Requiere hacer commit/push para cambiar imágenes
- ⚠️ El repositorio puede volverse grande

**¿Cómo funciona?**
- Las imágenes se guardan en `static/images/productos/`
- Se referencian en el código
- Se despliegan con el código

---

### Opción 3: Cargar Datos Sin Imágenes

**Ventajas:**
- ✅ Funciona inmediatamente
- ✅ No requiere configuración adicional
- ✅ Puedes agregar imágenes después

**Desventajas:**
- ⚠️ Los productos no tendrán imágenes inicialmente
- ⚠️ Necesitarás subir imágenes manualmente después

**¿Cómo funciona?**
- Cargas los productos con datos básicos (nombre, precio, stock)
- Las imágenes son opcionales
- Puedes agregarlas después con Cloudinary u otro servicio

---

## 🚀 Solución Recomendada: Cloudinary

### Paso 1: Crear Cuenta en Cloudinary

1. Ve a https://cloudinary.com
2. Haz clic en **"Sign Up for Free"**
3. Completa el formulario
4. Confirma tu email
5. Ve a tu **Dashboard**
6. Copia las credenciales:
   - **Cloud name**
   - **API Key**
   - **API Secret**

### Paso 2: Configurar Cloudinary en Django

**Instalar la librería:**
```bash
pip install django-cloudinary-storage
```

**Agregar a `requirements.txt`:**
```
django-cloudinary-storage>=0.3.0
```

**Configurar en `settings.py`:**
```python
# Agregar a INSTALLED_APPS
INSTALLED_APPS = [
    # ... otras apps
    'cloudinary',
    'cloudinary_storage',
]

# Configurar Cloudinary
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

# Usar Cloudinary para archivos media
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
```

**Configurar en Render:**
- Ve a tu servicio en Render
- Agrega estas variables de entorno:
  - `CLOUDINARY_CLOUD_NAME`: Tu cloud name
  - `CLOUDINARY_API_KEY`: Tu API key
  - `CLOUDINARY_API_SECRET`: Tu API secret

### Paso 3: Hacer Commit y Deploy

```bash
git add requirements.txt cadmium/settings.py
git commit -m "feat: Agregar Cloudinary para almacenamiento de imágenes"
git push origin main
```

---

## 📦 Solución Alternativa: Cargar Productos Automáticamente

Ya tienes un comando para cargar productos iniciales: `init_inventario`

**Puedo agregarlo al `build.sh` para que se ejecute automáticamente:**

```bash
python manage.py init_inventario
```

**Esto creará:**
- Todos los productos de bodega
- Todos los productos de mesón
- Todos los productos de limpieza

**Sin imágenes inicialmente** (las puedes agregar después)

---

## 🎯 ¿Qué Opción Elegir?

### Si necesitas imágenes que cambien frecuentemente:
→ **Usa Cloudinary** (Opción 1)

### Si las imágenes no cambian mucho:
→ **Usa archivos estáticos** (Opción 2)

### Si solo necesitas cargar los datos primero:
→ **Usa el comando `init_inventario`** (Opción 3)

---

## 📋 Plan de Acción Recomendado

1. **Ahora (Inmediato):**
   - Agregar `init_inventario` al `build.sh` para cargar productos automáticamente
   - Los productos se crearán sin imágenes

2. **Después (Opcional):**
   - Configurar Cloudinary para imágenes persistentes
   - Subir imágenes desde el panel (se guardarán en Cloudinary)

3. **Alternativa:**
   - Si las imágenes no cambian, inclúyelas como archivos estáticos en el repositorio

---

## 🛠️ ¿Qué Quieres Hacer?

Dime qué opción prefieres y te ayudo a implementarla:

1. **Configurar Cloudinary** (imágenes persistentes desde el panel)
2. **Agregar `init_inventario` al build** (cargar productos automáticamente)
3. **Ambas** (cargar productos + configurar Cloudinary)

---

## 💡 Nota Importante

**Render Free es perfecto para:**
- ✅ Base de datos (PostgreSQL)
- ✅ Código y archivos estáticos
- ✅ Aplicaciones Django

**Render Free NO es bueno para:**
- ❌ Archivos media (imágenes subidas por usuarios)
- ❌ Almacenamiento de archivos grandes
- ❌ Archivos que cambian frecuentemente

**Por eso necesitas Cloudinary u otro servicio de almacenamiento para las imágenes.**









