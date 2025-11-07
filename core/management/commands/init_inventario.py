from django.core.management.base import BaseCommand
from core.models import Inventario


class Command(BaseCommand):
    help = 'Inicializa los productos del inventario con las categorías y productos predeterminados'

    def handle(self, *args, **options):
        # Productos de Bodega
        productos_bodega = [
            'Agua (Bidones)',
            'Milo',
            'Leche',
            'Capuccino',
            'Capuccino Vainilla',
            'Mokaccino',
            'Cacao',
            'Café en Grano',
            'Tapas Pequeñas',
            'Tapas Grandes',
            'Vasos Pequeños',
            'Vasos Grandes',
            'Te Negro',
            'Te Verde',
            'Te Limon Jengibre'
        ]
        
        # Productos de Mesón
        productos_meson = [
            'Revolvedores',
            'Servilletas',
            'Azucar',
            'Sucralosa'
        ]
        
        # Productos de Limpieza
        productos_limpieza = [
            'Toalla de Papel',
            'Toalla Humeda',
            'Paños',
            'Traperos',
            'Bolsas de Basura Grandes',
            'Bolsas de Basura Pequeñas'
        ]
        
        # Crear productos de Bodega
        for producto in productos_bodega:
            inventario, created = Inventario.objects.get_or_create(
                nombre=producto,
                categoria='bodega',
                defaults={
                    'cantidad': 0,
                    'precio_unitario': 0.00,
                    'descripcion': f'Producto de bodega: {producto}'
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Producto creado: {producto} (Bodega)'))
            else:
                self.stdout.write(self.style.WARNING(f'Producto ya existe: {producto} (Bodega)'))
        
        # Crear productos de Mesón
        for producto in productos_meson:
            inventario, created = Inventario.objects.get_or_create(
                nombre=producto,
                categoria='meson',
                defaults={
                    'cantidad': 0,
                    'precio_unitario': 0.00,
                    'descripcion': f'Producto de mesón: {producto}'
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Producto creado: {producto} (Mesón)'))
            else:
                self.stdout.write(self.style.WARNING(f'Producto ya existe: {producto} (Mesón)'))
        
        # Crear productos de Limpieza
        for producto in productos_limpieza:
            inventario, created = Inventario.objects.get_or_create(
                nombre=producto,
                categoria='limpieza',
                defaults={
                    'cantidad': 0,
                    'precio_unitario': 0.00,
                    'descripcion': f'Producto de limpieza: {producto}'
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Producto creado: {producto} (Limpieza)'))
            else:
                self.stdout.write(self.style.WARNING(f'Producto ya existe: {producto} (Limpieza)'))
        
        self.stdout.write(self.style.SUCCESS('\nInventario inicializado correctamente.'))

