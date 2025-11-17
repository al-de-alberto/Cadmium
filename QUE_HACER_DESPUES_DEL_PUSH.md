# 🚀 Qué Hacer Después del Push - Crear Usuarios

## ✅ Paso 1: Esperar el Deploy Automático

Render detectará automáticamente el cambio en GitHub y comenzará un nuevo deploy.

**¿Cómo verificar?**
1. Ve a tu dashboard de Render: https://dashboard.render.com
2. Busca tu servicio web (Cadmium)
3. Verás el estado del deploy:
   - 🟡 **"Building"** = Está construyendo
   - 🟢 **"Live"** = Desplegado correctamente
   - 🔴 **"Failed"** = Hubo un error (revisa los logs)

**Tiempo estimado:** 3-5 minutos

---

## ✅ Paso 2: Verificar que el Usuario se Creó

Una vez que el deploy esté **"Live"**:

1. **Revisa los logs del build:**
   - En Render, ve a tu servicio
   - Haz clic en **"Logs"**
   - Busca esta línea:
     ```
     Usuario administrador "Gerencia" creado exitosamente
     ```
   - Si ves esto, el usuario se creó correctamente ✅

2. **Si el usuario ya existía:**
   - Verás: `El usuario "Gerencia" ya existe`
   - Esto es normal y no es un problema ✅

---

## ✅ Paso 3: Iniciar Sesión

1. **Ve a tu sitio web:**
   - URL: `https://tu-sitio.onrender.com` (o la URL que te dio Render)

2. **Haz clic en "Iniciar Sesión"**

3. **Ingresa las credenciales:**
   - **Usuario:** `Gerencia`
   - **Contraseña:** `Ger_2O25`
   - **Tipo de cuenta:** Selecciona "Administrador"

4. **Haz clic en "Iniciar Sesión"**

5. **Si es la primera vez:**
   - Te pedirá cambiar la contraseña
   - **¡Cámbiala a una más segura!** 🔒

---

## ✅ Paso 4: Cambiar la Contraseña (MUY IMPORTANTE)

**⚠️ IMPORTANTE:** La contraseña actual está en el código, así que debes cambiarla.

1. **Desde el panel de administración:**
   - Una vez dentro, ve a tu perfil o configuración
   - Busca la opción para cambiar contraseña
   - O desde el panel de usuarios, edita el usuario "Gerencia"

2. **Cambia a una contraseña segura:**
   - Mínimo 8 caracteres
   - Combina letras, números y símbolos
   - No uses información personal

---

## ✅ Paso 5: Crear Más Usuarios

Ahora que tienes acceso como administrador:

1. **Ve al Panel:**
   - Desde el menú, selecciona **"Panel"**

2. **Ve a Usuarios:**
   - Haz clic en **"Usuarios"** en el menú del panel

3. **Crear Nuevo Usuario:**
   - Haz clic en **"Crear Usuario"** o el botón **"+"**
   - Completa el formulario:
     - Username
     - Contraseña
     - Nombre
     - Apellido
     - RUT (opcional)
     - Correo (opcional)
     - Rol (Administrador o Empleado)
   - Haz clic en **"Guardar"**

4. **Repite para cada usuario que necesites**

---

## ✅ Paso 6: Cargar Datos Iniciales

### Inventario

1. **Ve a Panel → Inventario**
2. **Haz clic en "Crear Producto"**
3. **Completa el formulario:**
   - Nombre del producto
   - Categoría
   - Precio
   - Stock inicial
   - Descripción (opcional)
4. **Guarda**

### Asistencias

Las asistencias se crean cuando los empleados las registran desde su dashboard.

### Pedidos

Los pedidos se crean desde el panel de productos cuando los administradores los generan.

### Contenido (Carrusel, Eventos, Noticias)

1. **Carrusel:** Panel → Carrusel → Crear Imagen
2. **Eventos:** Panel → Eventos → Crear Evento
3. **Noticias:** Panel → Noticias → Crear Noticia

---

## 🔍 Solución de Problemas

### ❌ Error: "Usuario o contraseña incorrectos"

**Posibles causas:**
1. El deploy aún no terminó
   - **Solución:** Espera unos minutos y vuelve a intentar

2. El usuario no se creó
   - **Solución:** Revisa los logs del build en Render
   - Busca errores relacionados con `create_gerencia`

3. Escribiste mal las credenciales
   - **Solución:** Verifica que sea exactamente:
     - Usuario: `Gerencia` (con G mayúscula)
     - Contraseña: `Ger_2O25`

### ❌ Error: "Invalid HTTP_HOST header"

**Causa:** El dominio de Render no está en `ALLOWED_HOSTS`

**Solución:**
1. Ve a Render → Tu Servicio → Environment
2. Agrega el dominio a `ALLOWED_HOSTS`:
   ```
   cadmium-j4w7.onrender.com,tu-otro-dominio.com
   ```
3. Guarda y espera el redeploy

### ❌ El deploy falló

**Solución:**
1. Revisa los logs del build en Render
2. Busca el error específico
3. Si es un error de migraciones, verifica que las migraciones estén correctas
4. Si es un error de dependencias, verifica `requirements.txt`

---

## 📋 Checklist Post-Deploy

- [ ] Deploy completado y estado "Live" en Render
- [ ] Logs del build muestran que el usuario se creó correctamente
- [ ] Puedo iniciar sesión con "Gerencia" / "Ger_2O25"
- [ ] Cambié la contraseña de Gerencia a una más segura
- [ ] Creé los usuarios necesarios desde el panel
- [ ] Cargué los productos iniciales en el inventario
- [ ] Configuré el contenido inicial (carrusel, eventos, noticias)

---

## 🎉 ¡Listo!

Una vez completados estos pasos, tu aplicación estará lista para usar en producción.

**¿Necesitas ayuda?**
- Revisa los logs en Render
- Verifica la guía `CREAR_USUARIOS_SIN_SHELL.md`
- Revisa la documentación de Django y Render













