from django.core.management.base import BaseCommand
from core.models import Inventario


class Command(BaseCommand):
    help = 'Inicializa los productos del inventario con las categorías y productos predeterminados'

    def verificar_producto_existente(self, nombre_producto, categoria, nombres_alternativos=None):
        """
        Verifica si ya existe un producto en la categoría, considerando nombres alternativos.
        Retorna el producto existente si lo encuentra, None si no existe.
        """
        # Primero verificar si existe con el nombre exacto
        try:
            return Inventario.objects.get(nombre=nombre_producto, categoria=categoria)
        except Inventario.DoesNotExist:
            pass
        
        # Si hay nombres alternativos, verificar si existe alguno de esos
        if nombres_alternativos:
            for nombre_alt in nombres_alternativos:
                try:
                    return Inventario.objects.get(nombre=nombre_alt, categoria=categoria)
                except Inventario.DoesNotExist:
                    continue
        
        return None

    def handle(self, *args, **options):
        # Mapeo de productos con sus nombres alternativos (nombres antiguos o variantes)
        # Esto evita crear duplicados cuando un producto fue renombrado
        productos_config = {
            'bodega': {
                'Agua (Bidones)': ['Agua'],  # Si existe "Agua", no crear "Agua (Bidones)"
                'Milo': [],
                'Leche': [],
                'Capuccino': [],
                'Capuccino Vainilla': [],
                'Mokaccino': [],
                'Cacao': [],
                'Café en Grano': [],
                'Tapas Pequeñas': [],
                'Tapas Grandes': [],
                'Vasos Pequeños': [],
                'Vasos Grandes': [],
                'Te Negro': [],
                'Te Verde': [],
                'Te Limon Jengibre': []
            },
            'meson': {
                'Revolvedores': [],
                'Servilletas': [],
                'Azucar': [],
                'Sucralosa': []
            },
            'limpieza': {
                'Toalla de Papel': [],
                'Toalla Humeda': [],
                'Paños': [],
                'Traperos': [],
                'Bolsas de Basura Grandes': [],
                'Bolsas de Basura Pequeñas': []
            }
        }
        
        # Procesar cada categoría
        for categoria, productos in productos_config.items():
            for producto, nombres_alternativos in productos.items():
                # Verificar si ya existe el producto (con nombre exacto o alternativo)
                producto_existente = self.verificar_producto_existente(
                    producto, categoria, nombres_alternativos
                )
                
                if producto_existente:
                    # Si existe con otro nombre, informar pero no crear duplicado
                    if producto_existente.nombre != producto:
                        self.stdout.write(
                            self.style.WARNING(
                                f'Producto ya existe como "{producto_existente.nombre}" '
                                f'(se esperaba "{producto}") en {categoria.capitalize()}. '
                                f'No se creará duplicado.'
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f'Producto ya existe: {producto} ({categoria.capitalize()})'
                            )
                        )
                else:
                    # Crear el producto solo si no existe
                    inventario = Inventario.objects.create(
                        nombre=producto,
                        categoria=categoria,
                        cantidad=0,
                        precio_unitario=0.00,
                        descripcion=f'Producto de {categoria}: {producto}'
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Producto creado: {producto} ({categoria.capitalize()})'
                        )
                    )
        
        self.stdout.write(self.style.SUCCESS('\nInventario inicializado correctamente.'))

