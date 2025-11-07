"""
Script para ayudar a buscar y organizar imágenes de productos
Este script abre los sitios web en tu navegador para facilitar la descarga
"""

import webbrowser
import os
from pathlib import Path

# Mapeo de productos a búsquedas en Flaticon
PRODUCTOS_BUSQUEDAS = {
    # Bodega
    'Agua (Bidones)': 'water+bottle',
    'Milo': 'chocolate+drink',
    'Leche': 'milk+carton',
    'Capuccino': 'cappuccino',
    'Capuccino Vainilla': 'coffee+cup',
    'Mokaccino': 'mocha',
    'Cacao': 'cocoa',
    'Café en Grano': 'coffee+beans',
    'Tapas Pequeñas': 'cup+lid',
    'Tapas Grandes': 'cup+lid',
    'Vasos Pequeños': 'coffee+cup',
    'Vasos Grandes': 'coffee+cup+large',
    'Te Negro': 'black+tea',
    'Te Verde': 'green+tea',
    'Te Limon Jengibre': 'herbal+tea',
    
    # Mesón
    'Revolvedores': 'coffee+stirrer',
    'Servilletas': 'napkin',
    'Azucar': 'sugar',
    'Sucralosa': 'sweetener',
    
    # Limpieza
    'Toalla de Papel': 'paper+towel',
    'Toalla Humeda': 'wet+wipes',
    'Paños': 'cleaning+cloth',
    'Traperos': 'mop',
    'Bolsas de Basura Grandes': 'trash+bag',
    'Bolsas de Basura Pequeñas': 'trash+bag',
}

def abrir_busquedas_flaticon():
    """Abre Flaticon con búsquedas para cada producto"""
    base_url = "https://www.flaticon.com/search?word="
    
    print("=" * 70)
    print("Buscador de Imágenes - Flaticon")
    print("=" * 70)
    print("\nEste script abrirá Flaticon con búsquedas para cada producto.")
    print("Podrás descargar las imágenes directamente desde el navegador.\n")
    
    input("Presiona ENTER para comenzar (se abrirán múltiples pestañas)...")
    
    for producto, busqueda in PRODUCTOS_BUSQUEDAS.items():
        url = base_url + busqueda
        print(f"Abriendo: {producto} -> {url}")
        webbrowser.open(url)
        # Pequeña pausa para no sobrecargar
        import time
        time.sleep(1)
    
    print("\n✓ Todas las búsquedas se han abierto en tu navegador.")
    print("\n📝 RECORDATORIO:")
    print("1. Descarga cada imagen en formato PNG")
    print("2. Guarda en: static/images/inventario/")
    print("3. O súbelas desde el formulario de edición del producto")

def mostrar_info_descarga():
    """Muestra información sobre dónde descargar las imágenes"""
    print("\n" + "=" * 70)
    print("INFORMACIÓN DE DESCARGA")
    print("=" * 70)
    print("\n📁 Carpeta de destino: static/images/inventario/")
    print("\n📋 Productos a descargar:")
    
    categorias = {
        'BODEGA': ['Agua (Bidones)', 'Milo', 'Leche', 'Capuccino', 'Capuccino Vainilla', 
                   'Mokaccino', 'Cacao', 'Café en Grano', 'Tapas Pequeñas', 'Tapas Grandes',
                   'Vasos Pequeños', 'Vasos Grandes', 'Te Negro', 'Te Verde', 'Te Limon Jengibre'],
        'MESÓN': ['Revolvedores', 'Servilletas', 'Azucar', 'Sucralosa'],
        'LIMPIEZA': ['Toalla de Papel', 'Toalla Humeda', 'Paños', 'Traperos',
                     'Bolsas de Basura Grandes', 'Bolsas de Basura Pequeñas']
    }
    
    for categoria, productos in categorias.items():
        print(f"\n{categoria} ({len(productos)} productos):")
        for producto in productos:
            print(f"  - {producto}")
    
    print("\n" + "=" * 70)

if __name__ == '__main__':
    print("\n🔍 BUSCADOR DE IMÁGENES PARA INVENTARIO")
    print("=" * 70)
    print("\nOpciones:")
    print("1. Abrir Flaticon con búsquedas automáticas")
    print("2. Mostrar información de descarga")
    print("3. Ambos")
    
    opcion = input("\nSelecciona una opción (1/2/3): ").strip()
    
    if opcion == '1' or opcion == '3':
        abrir_busquedas_flaticon()
    
    if opcion == '2' or opcion == '3':
        mostrar_info_descarga()
    
    print("\n✅ ¡Listo! Revisa los archivos ENLACES_IMAGENES_INVENTARIO.md para más ayuda.")

