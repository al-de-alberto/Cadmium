# Generated manually

from django.db import migrations, models


def ensure_all_pedidos_have_codigo(apps, schema_editor):
    """Asegurar que todos los pedidos tengan un código"""
    Pedido = apps.get_model('core', 'Pedido')
    for pedido in Pedido.objects.filter(codigo__isnull=True) | Pedido.objects.filter(codigo=''):
        pedido.codigo = f'PEDIDO-{pedido.id}'
        pedido.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_remove_pedido_nombre_pedido_codigo_and_more'),
    ]

    operations = [
        # Primero asegurar que todos tengan código
        migrations.RunPython(ensure_all_pedidos_have_codigo, migrations.RunPython.noop),
        # Luego hacer el campo no nullable
        migrations.AlterField(
            model_name='pedido',
            name='codigo',
            field=models.CharField(max_length=200, verbose_name='Código del Pedido'),
        ),
    ]

