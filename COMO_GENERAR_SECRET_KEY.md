# 🔑 Cómo Generar la SECRET_KEY para Render

## 📍 ¿Dónde Generar la SECRET_KEY?

Generas la SECRET_KEY **en tu computadora local**, ejecutando el comando en PowerShell o Terminal.

---

## 🚀 Paso a Paso

### Paso 1: Abre PowerShell o Terminal

1. **Windows**: Presiona `Windows + X` y selecciona "Windows PowerShell" o "Terminal"
2. O busca "PowerShell" en el menú de inicio

### Paso 2: Navega a tu Proyecto (Opcional)

Si PowerShell no está en la carpeta del proyecto, navega ahí:

```powershell
cd "c:\0 INACAP\Cuarto Semestre\Ingenieria de Software\Cadmium"
```

### Paso 3: Ejecuta el Comando

Copia y pega este comando en PowerShell:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Paso 4: Copia el Resultado

El comando mostrará algo como esto:

```
django-insecure-abc123xyz789def456ghi012jkl345mno678pqr901stu234vwx567yz
```

**⚠️ IMPORTANTE:** Copia esta clave completa (es muy larga, asegúrate de copiar todo).

---

## 📝 ¿Qué Hacer con la SECRET_KEY?

### Opción 1: Guardarla Temporalmente (Recomendado)

1. **Copia la clave** que generó el comando
2. **Guárdala en un archivo temporal** o en un documento de texto
3. **NO la subas a GitHub** (ya está en `.gitignore`)
4. **La usarás** cuando configures las variables de entorno en Render

### Opción 2: Guardarla en un Archivo de Texto

Puedes guardarla en un archivo de texto (NO lo subas a GitHub):

```powershell
# Generar y guardar en un archivo
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" > secret_key.txt

# Ver el archivo
Get-Content secret_key.txt
```

**⚠️ IMPORTANTE:** Asegúrate de que `secret_key.txt` esté en `.gitignore` (ya debería estar excluido por `*.txt` o puedes agregarlo manualmente).

---

## 🎯 ¿Dónde se Usa la SECRET_KEY?

### En Render (Variables de Entorno)

Cuando crees el Web Service en Render, necesitarás:

1. **Ir a la sección "Environment Variables"**
2. **Agregar una nueva variable:**
   - **Key**: `SECRET_KEY`
   - **Value**: (pega la clave que generaste)
3. **Guardar**

### Ejemplo en Render

```
Variable: SECRET_KEY
Value: django-insecure-abc123xyz789def456ghi012jkl345mno678pqr901stu234vwx567yz
```

---

## ✅ Verificación

### Verificar que Funciona

Puedes verificar que la clave se generó correctamente:

```powershell
# Generar la clave
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Verificar la longitud (debe ser ~50 caracteres)
python -c "from django.core.management.utils import get_random_secret_key; key = get_random_secret_key(); print(f'Longitud: {len(key)} caracteres')"
```

---

## 🔒 Seguridad

### ⚠️ IMPORTANTE - Reglas de Seguridad

1. **NO la compartas públicamente**
2. **NO la subas a GitHub** (ya está en `.gitignore`)
3. **NO la hardcodees en el código** (ya está configurado para usar variable de entorno)
4. **Úsala SOLO en Render** (como variable de entorno)
5. **Guárdala en un lugar seguro** (archivo local, notas seguras, etc.)

---

## 📋 Checklist

- [ ] Ejecuté el comando en PowerShell
- [ ] Copié la SECRET_KEY generada
- [ ] La guardé en un lugar seguro
- [ ] Verifiqué que NO está en GitHub
- [ ] Estoy listo para usarla en Render

---

## 🚀 Siguiente Paso

Una vez que tengas la SECRET_KEY:

1. **Guárdala** en un lugar seguro
2. **Continúa con el deploy** en Render
3. **Configura la variable de entorno** `SECRET_KEY` en Render con este valor

**📖 Para más información sobre el deploy, consulta: `INSTRUCCIONES_RENDER_PASO_A_PASO.md`**

---

## ❓ Preguntas Frecuentes

### ¿Puedo usar la misma SECRET_KEY en desarrollo y producción?

**NO.** Es mejor tener una clave diferente para producción. La clave de desarrollo puede quedar en el código, pero la de producción debe ser única y segura.

### ¿Qué pasa si pierdo la SECRET_KEY?

Puedes generar una nueva en cualquier momento. Solo necesitas:
1. Generar una nueva clave
2. Actualizar la variable de entorno en Render
3. Render hará redeploy automáticamente

### ¿Necesito regenerar la SECRET_KEY cada vez?

**NO.** Solo necesitas generarla **una vez** para producción. La usarás siempre en Render (como variable de entorno).

---

## 🎉 ¡Listo!

Ya sabes cómo generar y usar la SECRET_KEY. Continúa con el deploy en Render.

**¡Buena suerte con el deploy!** 🚀

