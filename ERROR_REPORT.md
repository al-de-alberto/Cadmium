# Reporte de Errores y Problemas Encontrados

## Errores Críticos

### 1. Imports duplicados en `core/views.py`
- `Q` se importa al inicio (línea 7) pero también se importa dentro de funciones
- `Count`, `Avg`, `Max` se importan dentro de funciones cuando ya están disponibles

### 2. Statements de debugging en producción
- `print()` statements en líneas 2022, 2403, 2575 de `core/views.py`
- `console.warn()` en `templates/core/index.html` (líneas 218, 269)
- `print(traceback.format_exc())` en línea 2022 de `core/views.py`

### 3. Import de traceback no está en el inicio
- `traceback` se importa dentro de una función (línea 2021) en lugar de al inicio del archivo

## Advertencias del Linter

### 4. Errores de sintaxis en `templates/core/index.html`
- Línea 90: Errores de propiedad esperada (probablemente falso positivo del linter para HTML)

## Mejoras Recomendadas

### 5. Uso de logging en lugar de print
- Reemplazar todos los `print()` por `logging.error()` o `logging.debug()`

### 6. Imports innecesarios
- Revisar si todos los imports son necesarios

