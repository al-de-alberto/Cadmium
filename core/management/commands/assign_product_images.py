from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from core.models import Inventario
import os
import shutil


class Command(BaseCommand):
    help = 'Asigna imágenes a productos específicos del inventario'

    def handle(self, *args, **options):
        # Asegurar que el directorio media/inventario existe
        media_inventario_dir = settings.MEDIA_ROOT / 'inventario'
        media_inventario_dir.mkdir(parents=True, exist_ok=True)
        
        # Ruta de la imagen fuente (static) y destino (media)
        static_image_path = settings.BASE_DIR / 'static' / 'images' / 'inventario' / 'taza.png'
        media_image_path = media_inventario_dir / 'taza.png'
        
        # Verificar que la imagen fuente existe
        if not static_image_path.exists():
            self.stdout.write(self.style.ERROR(f'La imagen no existe en: {static_image_path}'))
            return
        
        # Copiar la imagen desde static a media si no existe
        if not media_image_path.exists():
            shutil.copy2(static_image_path, media_image_path)
            self.stdout.write(self.style.SUCCESS(f'Imagen copiada a: {media_image_path}'))
        else:
            self.stdout.write(self.style.WARNING(f'La imagen ya existe en: {media_image_path}'))
        
        # Productos a los que se asignará la imagen
        productos = ['Capuccino Vainilla', 'Mokaccino']
        
        # Asignar la imagen a cada producto
        for nombre_producto in productos:
            try:
                producto = Inventario.objects.get(nombre=nombre_producto)
                
                # Asignar la imagen
                with open(media_image_path, 'rb') as f:
                    producto.imagen.save('taza.png', File(f), save=True)
                
                self.stdout.write(self.style.SUCCESS(f'Imagen asignada a: {nombre_producto}'))
            except Inventario.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Producto no encontrado: {nombre_producto}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error al asignar imagen a {nombre_producto}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS('\nProceso completado.'))

