# 👥 Crear Usuarios SIN Shell de Render - Soluciones

## ⚠️ Problema: Shell de Render es de Pago

El Shell de Render es una característica del plan de pago. Si estás en el plan Free, no tienes acceso.

---

## ✅ Solución Implementada: Crear Superusuario Automáticamente

### ✅ **YA ESTÁ IMPLEMENTADO**

He modificado `build.sh` para que cree automáticamente el usuario administrador "Gerencia" después de las migraciones.

**¿Qué hace?**
- Se ejecuta automáticamente en cada deploy
- Crea el usuario "Gerencia" si no existe
- Si ya existe, no hace nada (no duplica usuarios)

**Credenciales del administrador:**
- Usuario: `Gerencia`
- Contraseña: `Ger_2O25`

---

## 🚀 Próximos Pasos

### 1. Hacer Commit y Push

Necesitas hacer commit y push de los cambios para que Render los aplique:

```bash
git add build.sh
git commit -m "feat: Crear usuario Gerencia automáticamente en build"
git push origin main
```

### 2. Esperar el Deploy

Render detectará el cambio y hará un nuevo deploy. El usuario "Gerencia" se creará automáticamente.

### 3. Iniciar Sesión

Una vez que el deploy termine:
1. Ve a tu sitio: `https://tu-sitio.onrender.com`
2. Haz clic en "Iniciar Sesión"
3. Usa las credenciales:
   - Usuario: `Gerencia`
   - Contraseña: `Ger_2O25`

### 4. Crear Más Usuarios

Una vez que inicies sesión como "Gerencia", puedes crear más usuarios desde el panel:

1. Ve a **Panel → Usuarios**
2. Haz clic en **"Crear Usuario"**
3. Completa el formulario
4. Guarda

---

## 📋 Crear Otros Datos Iniciales

### Inventario

Si necesitas cargar productos iniciales, puedes:

1. **Usar el Panel** (recomendado):
   - Inicia sesión como Gerencia
   - Ve a **Panel → Inventario**
   - Haz clic en **"Crear Producto"**
   - Completa el formulario

2. **Usar el Comando `init_inventario`** (si existe):
   - Necesitarías agregarlo al `build.sh` también
   - O crear una vista temporal para ejecutarlo

### Asistencias, Pedidos, etc.

Todos estos datos se pueden crear desde el panel una vez que tengas el usuario administrador.

---

## 🔒 Seguridad: Cambiar Contraseña

**IMPORTANTE:** Después de iniciar sesión por primera vez:

1. Ve a tu perfil o configuración
2. Cambia la contraseña de "Gerencia" a una más segura
3. La contraseña actual está en el código, así que es importante cambiarla

---

## 🛠️ Alternativas (Si Necesitas Más)

### Opción A: Crear Vista Temporal para Crear Usuarios

Si necesitas crear muchos usuarios rápidamente, puedo crear una vista temporal que:
- Solo sea accesible con una clave secreta en la URL
- Permita crear usuarios masivamente
- Se pueda eliminar después

### Opción B: Agregar Más Comandos al build.sh

Si tienes datos iniciales que siempre deben existir, puedo:
- Crear comandos de Django para cargarlos
- Agregarlos al `build.sh` para que se ejecuten automáticamente

---

## ✅ Resumen

1. ✅ **Ya está implementado**: El usuario "Gerencia" se creará automáticamente
2. ⏳ **Haz commit y push** de los cambios
3. ⏳ **Espera el deploy** en Render
4. ⏳ **Inicia sesión** con "Gerencia" / "Ger_2O25"
5. ⏳ **Crea más usuarios** desde el panel
6. ⏳ **Cambia la contraseña** de Gerencia por seguridad

