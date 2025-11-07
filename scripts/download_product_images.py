"""
Script para descargar imágenes de productos desde URLs
NOTA: Este script requiere que tengas las URLs de las imágenes
"""

import os
import requests
from pathlib import Path

# Mapeo de productos a nombres de archivo
PRODUCTOS_IMAGENES = {
    # Bodega
    'Agua (Bidones)': 'agua_bidones.png',
    'Milo': 'milo.png',
    'Leche': 'leche.png',
    'Capuccino': 'capuccino.png',
    'Capuccino Vainilla': 'capuccino_vainilla.png',
    'Mokaccino': 'mokaccino.png',
    'Cacao': 'cacao.png',
    'Café en Grano': 'cafe_grano.png',
    'Tapas Pequeñas': 'tapas_pequenas.png',
    'Tapas Grandes': 'tapas_grandes.png',
    'Vasos Pequeños': 'vasos_pequenos.png',
    'Vasos Grandes': 'vasos_grandes.png',
    'Te Negro': 'te_negro.png',
    'Te Verde': 'te_verde.png',
    'Te Limon Jengibre': 'te_limon_jengibre.png',
    
    # Mesón
    'Revolvedores': 'revolvedores.png',
    'Servilletas': 'servilletas.png',
    'Azucar': 'azucar.png',
    'Sucralosa': 'sucralosa.png',
    
    # Limpieza
    'Toalla de Papel': 'toalla_papel.png',
    'Toalla Humeda': 'toalla_humeda.png',
    'Paños': 'panos.png',
    'Traperos': 'traperos.png',
    'Bolsas de Basura Grandes': 'bolsas_basura_grandes.png',
    'Bolsas de Basura Pequeñas': 'bolsas_basura_pequenas.png',
}

# URLs de ejemplo (reemplazar con URLs reales)
URLS_IMAGENES = {
    # Estas URLs son ejemplos - necesitas reemplazarlas con URLs reales
    # Puedes obtenerlas de Flaticon, Icons8, etc.
}

def download_image(url, filepath):
    """Descarga una imagen desde una URL"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ Imagen descargada: {filepath.name}")
        return True
    except Exception as e:
        print(f"✗ Error al descargar {filepath.name}: {str(e)}")
        return False

def main():
    # Crear directorio si no existe
    base_dir = Path('static/images/inventario')
    base_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("Descargador de Imágenes de Productos")
    print("=" * 60)
    print("\nEste script descarga imágenes desde URLs.")
    print("Para usarlo, necesitas agregar las URLs en el diccionario URLS_IMAGENES\n")
    
    if not URLS_IMAGENES:
        print("⚠ No hay URLs configuradas.")
        print("\nPuedes:")
        print("1. Agregar URLs manualmente en este script")
        print("2. Descargar imágenes manualmente desde:")
        print("   - https://www.flaticon.com/")
        print("   - https://icons8.com/")
        print("   - https://www.freepik.com/")
        print("\n3. Guardarlas en: static/images/inventario/")
        print("\nNombres de archivo sugeridos:")
        for producto, filename in PRODUCTOS_IMAGENES.items():
            print(f"   {producto} -> {filename}")
        return
    
    # Descargar imágenes
    downloaded = 0
    for producto, filename in PRODUCTOS_IMAGENES.items():
        if producto in URLS_IMAGENES:
            filepath = base_dir / filename
            if download_image(URLS_IMAGENES[producto], filepath):
                downloaded += 1
    
    print(f"\n{'=' * 60}")
    print(f"Descargadas {downloaded} imágenes de {len(URLS_IMAGENES)} URLs configuradas")
    print(f"{'=' * 60}")

if __name__ == '__main__':
    main()

