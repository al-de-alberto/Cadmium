# 🎨 Guía: Aplicar Logo en Cadmium

## 📍 Ubicaciones del Logo

El logo se aplicará en **3 lugares**:

1. **Favicon** - Icono en la pestaña del navegador
2. **Navbar** - Logo en la barra de navegación (todos los templates)
3. **Index - App Icon** - Icono grande en la página principal

---

## 📁 Dónde Colocar el Logo

### Paso 1: Preparar el Logo

Necesitas **2 versiones** del logo:

1. **Logo para Favicon**: 
   - Formato: `.ico` o `.png`
   - Tamaño recomendado: 32x32px o 64x64px
   - Nombre: `favicon.ico` o `favicon.png`
   - Ubicación: `static/images/logo/`

2. **Logo para Navbar e Index**:
   - Formato: `.png` o `.svg` (recomendado SVG para mejor calidad)
   - Tamaño recomendado: 200x200px mínimo (se ajustará con CSS)
   - Nombre: `logo.png` o `logo.svg`
   - Ubicación: `static/images/logo/`

### Paso 2: Crear la Carpeta

```bash
# Crear la carpeta para el logo
mkdir static\images\logo
```

### Paso 3: Colocar los Archivos

Coloca tus archivos de logo en:
```
static/images/logo/
├── favicon.ico (o favicon.png)
└── logo.png (o logo.svg)
```

---

## ✅ Cambios Realizados en el Código

He actualizado el código para usar el logo. Los cambios incluyen:

### 1. **base.html** - Favicon
- Agregado `<link rel="icon">` para el favicon
- Funciona con `.ico` o `.png`

### 2. **navbar_snippet.html** - Logo en Navbar
- Reemplazado el texto "C" con imagen del logo
- Si el logo no existe, mostrará el texto "C" como fallback

### 3. **index.html** - Logo en App Icon Section
- Reemplazado el texto "C" con imagen del logo
- Si el logo no existe, mostrará el texto "C" como fallback

### 4. **CSS** - Estilos Actualizados
- Estilos para que el logo se vea bien en navbar (40x40px)
- Estilos para que el logo se vea bien en app-icon (120x120px)
- Transiciones suaves

---

## 🚀 Cómo Aplicar el Logo

### ✅ Cambios Realizados

**Ya he actualizado el código** para usar el logo automáticamente. Solo necesitas:

1. Colocar los archivos del logo en `static/images/logo/`:
   - `favicon.ico` (o `favicon.png`)
   - `logo.png` (o `logo.svg`)

2. El sistema detectará automáticamente el logo y lo usará.

### Opción A: Antes del Deploy (Recomendado)

1. Coloca los archivos del logo en `static/images/logo/`:
   - `favicon.ico` (o `favicon.png`)
   - `logo.png` (o `logo.svg`)

2. Verifica que los archivos estén en la carpeta:
   ```bash
   dir static\images\logo
   ```

3. Haz commit y push:
   ```bash
   git add static/images/logo/
   git commit -m "Agregar logo de Cadmium"
   git push origin main
   ```

4. El logo se aplicará automáticamente en el deploy

### Opción B: Después del Deploy

**SÍ, puedes actualizar el código después del deploy sin problemas.** Esto es lo normal:

1. Coloca los archivos del logo en `static/images/logo/`
2. Haz commit y push:
   ```bash
   git add static/images/logo/
   git commit -m "Agregar logo de Cadmium"
   git push origin main
   ```
3. Render detectará el cambio y hará redeploy automáticamente
4. El logo aparecerá en la aplicación desplegada

### Opción C: Subir Manualmente a Render (No Recomendado)

1. Sube los archivos del logo a Render usando Render Shell:
   ```bash
   # Desde Render Shell
   mkdir -p static/images/logo
   # Luego sube los archivos manualmente o desde el admin
   ```

2. O actualiza el código y haz redeploy:
   - Coloca los archivos en `static/images/logo/`
   - Haz commit y push
   - Render hará redeploy automáticamente

---

## 🔍 Verificar que Funciona

### Localmente

1. Ejecuta el servidor:
   ```bash
   python manage.py runserver
   ```

2. Verifica:
   - ✅ Favicon aparece en la pestaña del navegador
   - ✅ Logo aparece en la navbar
   - ✅ Logo aparece en la página principal (index)

### En Producción (Render)

1. Después del deploy, verifica:
   - ✅ Favicon aparece en la pestaña
   - ✅ Logo aparece en la navbar
   - ✅ Logo aparece en la página principal

---

## 📝 Notas Importantes

### Formatos Soportados

- **Favicon**: `.ico`, `.png`, `.svg`
- **Logo**: `.png`, `.svg`, `.jpg` (SVG recomendado)

### Tamaños Recomendados

- **Favicon**: 32x32px o 64x64px
- **Logo Navbar**: 200x200px mínimo (se ajusta a 40x40px)
- **Logo App Icon**: 200x200px mínimo (se ajusta a 120x120px)

### Fallback

Si el logo no existe, el sistema mostrará:
- **Navbar**: Texto "C" (como antes)
- **App Icon**: Texto "C" (como antes)
- **Favicon**: No mostrará nada (comportamiento normal del navegador)

---

## 🛠️ Troubleshooting

### El logo no aparece

1. **Verifica la ruta**:
   - Debe ser: `static/images/logo/logo.png`
   - No: `static/images/logo.png`

2. **Verifica los permisos**:
   - Los archivos deben ser accesibles

3. **Limpia la caché del navegador**:
   - Presiona `Ctrl + Shift + R` (Windows) o `Cmd + Shift + R` (Mac)

4. **Verifica collectstatic**:
   - En producción, ejecuta: `python manage.py collectstatic`

### El favicon no aparece

1. **Verifica el formato**:
   - `.ico` es el más compatible
   - `.png` también funciona

2. **Limpia la caché del navegador**:
   - Los favicons se cachean fuertemente

3. **Verifica la ruta en base.html**:
   - Debe apuntar a `static/images/logo/favicon.ico`

---

## ✅ Checklist

- [ ] Logo preparado en 2 versiones (favicon + logo)
- [ ] Carpeta `static/images/logo/` creada
- [ ] Archivos colocados en la carpeta
- [ ] Verificado localmente
- [ ] Commit y push realizado (si aplica)
- [ ] Verificado en producción (después del deploy)

---

## 🎉 ¡Listo!

Una vez que coloques los archivos del logo en `static/images/logo/`, el sistema los usará automáticamente. No necesitas hacer ningún cambio adicional en el código.

**¿Necesitas ayuda?** Revisa la sección de Troubleshooting o consulta la documentación de Django sobre archivos estáticos.

