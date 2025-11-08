"""
URL configuration for cadmium project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import os

# Configurar título del admin
admin.site.site_header = "Cadmium - Administración"
admin.site.site_title = "Cadmium Admin"
admin.site.index_title = "Panel de Administración"

# URL del admin: Usar variable de entorno o valor por defecto seguro
# En producción, cambia ADMIN_URL en variables de entorno a algo único
ADMIN_URL = os.environ.get('ADMIN_URL', 'admin-cadmium-secreto-2025/')

urlpatterns = [
    path(ADMIN_URL, admin.site.urls),  # URL personalizada del admin
    path('', include('core.urls')),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

