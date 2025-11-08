/**
 * Logo Loader - Maneja el fallback del logo
 * Si PNG falla, intenta SVG. Si ambos fallan, muestra el texto "C"
 */

// Función global para manejar errores de carga del logo
function handleLogoError(img) {
    const svgPath = img.getAttribute('data-logo-svg');
    const fallback = img.parentElement.querySelector('.logo-fallback');
    
    if (svgPath && img.src !== svgPath) {
        // Intentar cargar SVG
        img.src = svgPath;
        img.onerror = function() {
            // Si SVG también falla, mostrar fallback de texto
            img.style.display = 'none';
            if (fallback) {
                fallback.style.display = 'block';
            } else {
                // Crear fallback si no existe
                const span = document.createElement('span');
                span.className = 'logo-fallback';
                span.textContent = 'C';
                if (img.parentElement.classList.contains('app-icon')) {
                    span.style.fontSize = '4.5rem';
                    span.style.fontWeight = 'bold';
                }
                img.parentElement.appendChild(span);
            }
        };
    } else {
        // Si ya intentamos SVG o no hay SVG, mostrar fallback
        img.style.display = 'none';
        if (fallback) {
            fallback.style.display = 'block';
        } else {
            // Crear fallback si no existe
            const span = document.createElement('span');
            span.className = 'logo-fallback';
            span.textContent = 'C';
            if (img.parentElement.classList.contains('app-icon')) {
                span.style.fontSize = '4.5rem';
                span.style.fontWeight = 'bold';
            }
            img.parentElement.appendChild(span);
        }
    }
}

