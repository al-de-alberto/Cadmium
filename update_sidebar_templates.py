#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script para actualizar todos los templates del panel con las nuevas opciones del sidebar"""

import os
import re

# Lista de templates que necesitan actualización
templates_to_update = [
    'templates/core/usuarios.html',
    'templates/core/inventario.html',
    'templates/core/asistencia.html',
    'templates/core/ventas_pedidos.html',
    'templates/core/deliverys.html',
    'templates/core/operaciones.html',
    'templates/core/auditoria.html',
    'templates/core/crear_usuario.html',
    'templates/core/editar_usuario.html',
    'templates/core/eliminar_usuario.html',
    'templates/core/crear_inventario.html',
    'templates/core/editar_inventario.html',
    'templates/core/eliminar_inventario.html',
    'templates/core/crear_pedido.html',
    'templates/core/eliminar_pedido.html',
    'templates/core/crear_falla.html',
    'templates/core/editar_falla.html',
    'templates/core/eliminar_falla.html',
    'templates/core/crear_llamada.html',
    'templates/core/editar_llamada.html',
    'templates/core/eliminar_llamada.html',
    'templates/core/editar_asistencia.html',
    'templates/core/eliminar_asistencia.html',
]

# Nuevas opciones del sidebar a insertar
new_sidebar_options = '''            <a href="{% url 'gestionar_carrusel' %}" class="nav-item {% if request.resolver_match.url_name == 'gestionar_carrusel' or request.resolver_match.url_name == 'crear_imagen_carrusel' or request.resolver_match.url_name == 'editar_imagen_carrusel' %}active{% endif %}">
                <span class="nav-icon">🖼️</span>
                <span>Carrusel</span>
            </a>
            <a href="{% url 'gestionar_eventos' %}" class="nav-item {% if request.resolver_match.url_name == 'gestionar_eventos' or request.resolver_match.url_name == 'crear_evento' or request.resolver_match.url_name == 'editar_evento' %}active{% endif %}">
                <span class="nav-icon">📅</span>
                <span>Eventos</span>
            </a>
            <a href="{% url 'gestionar_noticias' %}" class="nav-item {% if request.resolver_match.url_name == 'gestionar_noticias' or request.resolver_match.url_name == 'crear_noticia' or request.resolver_match.url_name == 'editar_noticia' %}active{% endif %}">
                <span class="nav-icon">📰</span>
                <span>Noticias</span>
            </a>
'''

# Patrón para encontrar la línea antes de auditoría
pattern = r'(<a href="{% url \'operaciones\' %}"[^>]*>[\s\S]*?Operaciones</span>\s*</a>\s*)<a href="{% url \'auditoria\' %}"'

replacement = r'\1' + new_sidebar_options + '\n            <a href="{% url \'auditoria\' %}'

updated_count = 0

for template_path in templates_to_update:
    if not os.path.exists(template_path):
        print(f"Template no encontrado: {template_path}")
        continue
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar si ya tiene las nuevas opciones
        if 'gestionar_carrusel' in content and 'gestionar_eventos' in content:
            print(f"Ya actualizado: {template_path}")
            continue
        
        # Buscar el patrón y reemplazar
        new_content = re.sub(
            pattern,
            replacement,
            content,
            flags=re.MULTILINE
        )
        
        # Si no se encontró el patrón exacto, intentar otra estrategia
        if new_content == content:
            # Buscar la línea de auditoría y agregar antes
            audit_pattern = r'(<a href="{% url \'auditoria\' %}"[^>]*>[\s\S]*?Auditoría</span>\s*</a>)'
            audit_replacement = new_sidebar_options + '\n            ' + r'\1'
            new_content = re.sub(audit_pattern, audit_replacement, content, flags=re.MULTILINE)
        
        if new_content != content:
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Actualizado: {template_path}")
            updated_count += 1
        else:
            print(f"No se pudo actualizar (patrón no encontrado): {template_path}")
    
    except Exception as e:
        print(f"Error actualizando {template_path}: {e}")

print(f"\nTotal de templates actualizados: {updated_count}")

