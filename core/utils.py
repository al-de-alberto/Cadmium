"""
Utilidades para el sistema de auditoría
"""
import json
from django.utils import timezone
from .models import Auditoria


def registrar_auditoria(usuario, accion, modulo, descripcion, objeto_afectado=None, detalles=None):
    """
    Registra una acción en el sistema de auditoría
    
    Args:
        usuario: Usuario que realiza la acción (puede ser None)
        accion: Tipo de acción (debe ser una de las opciones en ACCION_CHOICES)
        modulo: Módulo afectado (debe ser una de las opciones en MODULO_CHOICES)
        descripcion: Descripción de la acción
        objeto_afectado: Nombre del objeto afectado (opcional)
        detalles: Diccionario con detalles adicionales (opcional, se convertirá a JSON)
    
    Returns:
        Instancia del registro de auditoría creado
    """
    detalles_json = None
    if detalles:
        try:
            detalles_json = json.dumps(detalles, ensure_ascii=False, default=str)
        except (TypeError, ValueError):
            detalles_json = str(detalles)
    
    registro = Auditoria.objects.create(
        usuario=usuario,
        accion=accion,
        modulo=modulo,
        descripcion=descripcion,
        objeto_afectado=objeto_afectado,
        detalles=detalles_json,
        fecha_hora=timezone.localtime(timezone.now())
    )
    
    return registro

