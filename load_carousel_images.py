"""
Script para cargar las imágenes del carrusel desde la carpeta imagenes/
"""
import os
import shutil
from pathlib import Path
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cadmium.settings')
django.setup()

from core.models import ImagenCarrusel

# Configuración de rutas
BASE_DIR = Path(__file__).resolve().parent
IMAGENES_DIR = BASE_DIR / 'imagenes'
MEDIA_CAROUSEL_DIR = BASE_DIR / 'media' / 'carousel'

# Crear directorio media/carousel si no existe
MEDIA_CAROUSEL_DIR.mkdir(parents=True, exist_ok=True)

# Mapeo de imágenes a orden (puedes ajustar el orden aquí)
IMAGENES_ORDEN = [
    ('nescafe.jpeg', 1),
    ('naya.jpeg', 2),
    ('halloween.jpeg', 3),
    ('jojos.jpeg', 4),
    ('payaso.jpeg', 5),
]

def cargar_imagenes():
    """Carga las imágenes en el carrusel"""
    # Limpiar imágenes existentes del carrusel (opcional - comentar si quieres mantener las existentes)
    # ImagenCarrusel.objects.all().delete()
    
    # Eliminar imágenes físicas existentes en media/carousel (opcional)
    # for file in MEDIA_CAROUSEL_DIR.glob('*'):
    #     if file.is_file():
    #         file.unlink()
    
    print("Iniciando carga de imágenes del carrusel...")
    
    for nombre_archivo, orden in IMAGENES_ORDEN:
        imagen_path = IMAGENES_DIR / nombre_archivo
        
        if not imagen_path.exists():
            print(f"[ADVERTENCIA] No se encontro {nombre_archivo}")
            continue
        
        # Copiar imagen a media/carousel
        destino_path = MEDIA_CAROUSEL_DIR / nombre_archivo
        shutil.copy2(imagen_path, destino_path)
        print(f"[OK] Copiado: {nombre_archivo} -> media/carousel/")
        
        # Verificar si ya existe una imagen con este orden
        imagen_existente = ImagenCarrusel.objects.filter(orden=orden).first()
        
        if imagen_existente:
            # Actualizar la imagen existente - abrir el archivo y asignarlo correctamente
            with open(destino_path, 'rb') as f:
                from django.core.files import File
                imagen_existente.imagen.save(nombre_archivo, File(f), save=True)
            imagen_existente.activo = True
            imagen_existente.save()
            print(f"[OK] Actualizado registro en orden {orden}: {nombre_archivo}")
        else:
            # Crear nuevo registro - abrir el archivo y asignarlo correctamente
            with open(destino_path, 'rb') as f:
                from django.core.files import File
                nueva_imagen = ImagenCarrusel(
                    orden=orden,
                    activo=True,
                    titulo_barista='Barista del Mes' if orden == 1 else None
                )
                nueva_imagen.imagen.save(nombre_archivo, File(f), save=True)
            print(f"[OK] Creado registro en orden {orden}: {nombre_archivo}")
    
    print("\n[COMPLETADO] Proceso completado!")
    print(f"\nTotal de imagenes en el carrusel: {ImagenCarrusel.objects.filter(activo=True).count()}")

if __name__ == '__main__':
    cargar_imagenes()

