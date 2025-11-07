# Imágenes Precargadas del Carrusel

Esta carpeta contiene las imágenes precargadas que se mostrarán en el carrusel de la página principal cuando no haya imágenes cargadas en la base de datos.

## Estructura

Coloca aquí las siguientes imágenes con estos nombres exactos:

- `carousel1.jpg`
- `carousel2.jpg`
- `carousel3.jpg`
- `carousel4.jpg`
- `carousel5.jpg`

## Recomendaciones

- **Formato**: JPG, PNG o JPEG
- **Tamaño recomendado**: 1920x1080 píxeles (Full HD) o superior
- **Tamaño de archivo**: Máximo 5MB por imagen
- **Aspecto**: 16:9 (landscape/horizontal) para mejor visualización
- **Contenido**: Imágenes relacionadas con PopUp Nescafe, productos, eventos, o el local

## Notas

- Estas imágenes se mostrarán automáticamente si no hay suficientes imágenes cargadas en el sistema
- El sistema siempre mostrará exactamente 5 imágenes en el carrusel
- Si hay imágenes cargadas en la base de datos, estas se mostrarán primero, y las imágenes precargadas completarán hasta llegar a 5

## Despliegue

Al hacer `python manage.py collectstatic`, estas imágenes se copiarán a la carpeta `staticfiles/` para su uso en producción.

