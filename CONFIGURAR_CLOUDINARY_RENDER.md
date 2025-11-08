# ☁️ Configurar Cloudinary en Render

## ✅ Código Ya Configurado

El código ya está preparado para usar Cloudinary. Solo necesitas:

1. Crear cuenta en Cloudinary (gratis)
2. Obtener las credenciales
3. Agregarlas en Render

---

## 📝 Paso 1: Crear Cuenta en Cloudinary

1. **Ve a:** https://cloudinary.com
2. **Haz clic en:** "Sign Up for Free"
3. **Completa el formulario:**
   - Email
   - Nombre
   - Contraseña
   - Organización (opcional)
4. **Confirma tu email** (revisa tu bandeja de entrada)
5. **Inicia sesión**

---

## 🔑 Paso 2: Obtener Credenciales

1. **Una vez dentro del Dashboard:**
   - Verás un resumen con tus credenciales
   - O ve a la sección **"Settings"** (Configuración)

2. **Copia estas 3 credenciales:**
   - **Cloud Name** (ej: `dxyz1234`)
   - **API Key** (ej: `123456789012345`)
   - **API Secret** (ej: `abcdefghijklmnopqrstuvwxyz123456`)

   ⚠️ **IMPORTANTE:** Guarda estas credenciales en un lugar seguro.

---

## 🚀 Paso 3: Configurar en Render

1. **Ve a tu servicio en Render:**
   - https://dashboard.render.com
   - Busca tu servicio web (Cadmium)

2. **Ve a la sección "Environment":**
   - En el menú lateral, haz clic en **"Environment"**

3. **Agrega estas 3 variables de entorno:**
   
   **Variable 1:**
   - **Key:** `CLOUDINARY_CLOUD_NAME`
   - **Value:** Tu Cloud Name (ej: `dxyz1234`)
   
   **Variable 2:**
   - **Key:** `CLOUDINARY_API_KEY`
   - **Value:** Tu API Key (ej: `123456789012345`)
   
   **Variable 3:**
   - **Key:** `CLOUDINARY_API_SECRET`
   - **Value:** Tu API Secret (ej: `abcdefghijklmnopqrstuvwxyz123456`)

4. **Haz clic en "Save Changes"**

---

## ⏳ Paso 4: Esperar el Deploy

**Render detectará las nuevas variables de entorno y hará un deploy automático.**

**Tiempo estimado:** 3-5 minutos

---

## ✅ Paso 5: Probar la Carga de Imágenes

**Una vez que el deploy termine:**

1. **Ve a tu sitio:** `https://tu-sitio.onrender.com`
2. **Inicia sesión** con tu usuario administrador
3. **Ve a:** Panel → Inventario → Crear Producto
4. **Intenta subir una imagen:**
   - Haz clic en "Examinar"
   - Selecciona una imagen
   - Completa los demás campos
   - Haz clic en "Crear Producto"

5. **Verifica:**
   - ✅ La imagen se sube correctamente
   - ✅ La imagen se muestra en el listado
   - ✅ La imagen persiste después de reiniciar el servicio

---

## 🎉 ¡Listo!

**Después de configurar Cloudinary:**
- ✅ Las imágenes se suben correctamente
- ✅ Se almacenan permanentemente en la nube
- ✅ Se sirven desde la CDN de Cloudinary (carga rápida)
- ✅ No se pierden al reiniciar el servicio

---

## 🔍 Verificar que Funciona

**Para verificar que Cloudinary está configurado:**

1. **Ve a los logs de Render:**
   - Si hay errores, aparecerán en los logs

2. **Prueba subir una imagen:**
   - Si funciona, la imagen se mostrará correctamente
   - Si no funciona, revisa los logs para ver el error

3. **Revisa tu cuenta de Cloudinary:**
   - Ve a tu Dashboard de Cloudinary
   - En la sección "Media Library", deberías ver las imágenes que subes

---

## ❌ Solución de Problemas

### Error: "CLOUDINARY_CLOUD_NAME not set"

**Causa:** Las variables de entorno no están configuradas en Render.

**Solución:**
1. Verifica que agregaste las 3 variables en Render
2. Verifica que los nombres de las variables sean exactamente:
   - `CLOUDINARY_CLOUD_NAME`
   - `CLOUDINARY_API_KEY`
   - `CLOUDINARY_API_SECRET`
3. Verifica que los valores sean correctos (sin espacios al inicio/final)
4. Guarda los cambios en Render
5. Espera el redeploy

### Error: "Invalid API credentials"

**Causa:** Las credenciales son incorrectas.

**Solución:**
1. Verifica que copiaste las credenciales correctamente
2. Verifica que no hay espacios al inicio/final
3. Obtén las credenciales nuevamente desde Cloudinary
4. Actualiza las variables en Render
5. Espera el redeploy

### La imagen no se muestra

**Causa:** Puede ser un problema de permisos o configuración.

**Solución:**
1. Verifica que la imagen se subió correctamente (revisa los logs)
2. Verifica que la imagen existe en Cloudinary (Media Library)
3. Verifica que la URL de la imagen es correcta
4. Revisa la consola del navegador para ver errores

---

## 💡 Notas Importantes

1. **Gratis hasta 25 GB:**
   - Cloudinary tiene un plan gratuito con 25 GB de almacenamiento
   - Es suficiente para muchas aplicaciones

2. **CDN incluido:**
   - Las imágenes se sirven desde una CDN global
   - Carga rápida en todo el mundo

3. **Transformaciones:**
   - Cloudinary permite transformar imágenes automáticamente
   - Puedes redimensionar, recortar, etc. sin procesamiento adicional

4. **Seguridad:**
   - Las credenciales están en variables de entorno
   - No se exponen en el código
   - Son seguras

---

## 🎯 Resumen

1. ✅ Código configurado
2. ⏳ Crear cuenta en Cloudinary
3. ⏳ Obtener credenciales
4. ⏳ Agregar variables de entorno en Render
5. ⏳ Esperar deploy
6. ⏳ Probar carga de imágenes

**¿Necesitas ayuda?** Revisa los logs de Render o contacta con soporte.

