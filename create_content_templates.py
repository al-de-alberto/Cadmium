#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script para crear templates de eventos y noticias"""

# Template base para gestionar eventos
gestionar_eventos = '''{% extends 'core/base.html' %}
{% load static %}

{% block title %}Gestionar Eventos - Cadmium{% endblock %}

{% block content %}
{% include 'core/navbar_snippet.html' %}

<div class="admin-container">
    <aside class="sidebar">
        <div class="sidebar-header">
            <a href="{% url 'index' %}" style="text-decoration: none; color: inherit;">
                <h2>Cadmium</h2>
            </a>
            <p>Panel de Administración</p>
        </div>
        
        <nav class="sidebar-nav">
            <a href="{% url 'panel' %}" class="nav-item {% if request.resolver_match.url_name == 'panel' %}active{% endif %}">
                <span class="nav-icon">📊</span>
                <span>Dashboard</span>
            </a>
            <a href="{% url 'usuarios' %}" class="nav-item {% if request.resolver_match.url_name == 'usuarios' %}active{% endif %}">
                <span class="nav-icon">👥</span>
                <span>Usuarios</span>
            </a>
            <a href="{% url 'inventario' %}" class="nav-item {% if request.resolver_match.url_name == 'inventario' %}active{% endif %}">
                <span class="nav-icon">📦</span>
                <span>Inventario</span>
            </a>
            <a href="{% url 'ventas_pedidos' %}" class="nav-item {% if request.resolver_match.url_name == 'ventas_pedidos' %}active{% endif %}">
                <span class="nav-icon">💰</span>
                <span>Productos</span>
            </a>
            <a href="{% url 'asistencia' %}" class="nav-item {% if request.resolver_match.url_name == 'asistencia' %}active{% endif %}">
                <span class="nav-icon">📅</span>
                <span>Asistencia</span>
            </a>
            <a href="{% url 'deliverys' %}" class="nav-item {% if request.resolver_match.url_name == 'deliverys' %}active{% endif %}">
                <span class="nav-icon">🚚</span>
                <span>Delivery</span>
            </a>
            <a href="{% url 'operaciones' %}" class="nav-item {% if request.resolver_match.url_name == 'operaciones' %}active{% endif %}">
                <span class="nav-icon">⚙️</span>
                <span>Operaciones</span>
            </a>
            <a href="{% url 'gestionar_carrusel' %}" class="nav-item {% if request.resolver_match.url_name == 'gestionar_carrusel' or request.resolver_match.url_name == 'crear_imagen_carrusel' or request.resolver_match.url_name == 'editar_imagen_carrusel' %}active{% endif %}">
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
            <a href="{% url 'auditoria' %}" class="nav-item {% if request.resolver_match.url_name == 'auditoria' %}active{% endif %}">
                <span class="nav-icon">📋</span>
                <span>Auditoría</span>
            </a>
        </nav>
        
        <div class="sidebar-footer">
            <div class="user-info">
                <p><strong>{{ user.username }}</strong></p>
                <p class="user-role">{{ user.get_rol_display }}</p>
            </div>
        </div>
    </aside>
    
    <main class="main-content">
        <header class="content-header">
            <h1>Gestión de Eventos</h1>
            <div class="header-actions">
                <a href="{% url 'crear_evento' %}" class="btn btn-primary">+ Crear Evento</a>
                <a href="{% url 'panel' %}" class="btn btn-secondary">← Volver</a>
            </div>
        </header>
        
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }}">
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}
        
        <div class="table-container">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Título</th>
                        <th>Fecha del Evento</th>
                        <th>Estado</th>
                        <th>Fecha Creación</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {% for evento in eventos %}
                    <tr>
                        <td><strong>{{ evento.titulo }}</strong></td>
                        <td>{{ evento.fecha_evento|date:"d/m/Y" }}</td>
                        <td>
                            {% if evento.activo %}
                                <span class="badge badge-success">Activo</span>
                            {% else %}
                                <span class="badge badge-danger">Inactivo</span>
                            {% endif %}
                        </td>
                        <td>{{ evento.fecha_creacion|date:"d/m/Y H:i" }}</td>
                        <td>
                            <div class="action-buttons">
                                <a href="{% url 'editar_evento' evento.id %}" class="btn-action btn-edit" title="Modificar">
                                    <span class="icon-edit">↻</span>
                                </a>
                                <a href="{% url 'eliminar_evento' evento.id %}" class="btn-action btn-delete" title="Eliminar">
                                    <span class="icon-delete">🗑️</span>
                                </a>
                            </div>
                        </td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="5" class="text-center">No hay eventos registrados</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </main>
</div>

<style>
.action-buttons {
    display: flex;
    gap: 8px;
    justify-content: center;
    align-items: center;
}

.btn-action {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border-radius: 6px;
    text-decoration: none;
    transition: all 0.3s ease;
    font-size: 18px;
    border: none;
    cursor: pointer;
}

.btn-edit {
    background: linear-gradient(135deg, var(--warning-color) 0%, #FFD700 100%);
    color: var(--text-primary);
    box-shadow: 0 2px 6px rgba(245, 203, 92, 0.3);
}

.btn-edit:hover {
    background: linear-gradient(135deg, #FFD700 0%, var(--warning-color) 100%);
    transform: translateY(-2px);
    box-shadow: 0 4px 10px rgba(245, 203, 92, 0.5);
}

.btn-delete {
    background: linear-gradient(135deg, var(--danger-color) 0%, #E53935 100%);
    color: white;
    box-shadow: 0 2px 6px rgba(198, 40, 40, 0.3);
}

.btn-delete:hover {
    background: linear-gradient(135deg, #E53935 0%, var(--danger-color) 100%);
    transform: translateY(-2px);
    box-shadow: 0 4px 10px rgba(198, 40, 40, 0.5);
}

.icon-edit, .icon-delete {
    display: inline-block;
    font-size: 18px;
    line-height: 1;
}

.data-table th:last-child,
.data-table td:last-child {
    text-align: center;
    width: 100px;
}
</style>
{% endblock %}
'''

with open('templates/core/gestionar_eventos.html', 'w', encoding='utf-8') as f:
    f.write(gestionar_eventos)

print("gestionar_eventos.html creado")

