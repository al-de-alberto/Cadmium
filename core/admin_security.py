"""
Middleware y utilidades para mejorar la seguridad del Django Admin
"""
import time
import logging
import os
from django.core.cache import cache
from django.http import HttpResponseForbidden, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import resolve, reverse
from django.utils import timezone

logger = logging.getLogger('django.security')


def get_admin_url_path():
    """
    Obtiene la ruta del admin configurada.
    Usa la misma lógica que urls.py
    """
    admin_url = os.environ.get('ADMIN_URL', 'admin-cadmium-secreto-2025/')
    # Normalizar: remover barra inicial si existe, agregar al final
    if admin_url.startswith('/'):
        admin_url = admin_url[1:]
    if not admin_url.endswith('/'):
        admin_url += '/'
    return f'/{admin_url}'


class AdminSecurityMiddleware(MiddlewareMixin):
    """
    Middleware para proteger el Django Admin con:
    - Rate limiting (límite de requests por IP)
    - Protección contra fuerza bruta (bloqueo después de intentos fallidos)
    - Logging de accesos al admin
    """
    
    # Configuración
    MAX_LOGIN_ATTEMPTS = 5  # Número máximo de intentos de login fallidos
    LOCKOUT_TIME = 900  # Tiempo de bloqueo en segundos (15 minutos)
    RATE_LIMIT_REQUESTS = 60  # Máximo de requests por ventana de tiempo
    RATE_LIMIT_WINDOW = 60  # Ventana de tiempo en segundos (1 minuto)
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
    
    def process_request(self, request):
        """Procesa cada request antes de que llegue a la vista"""
        
        # Solo aplicar a rutas del admin (usar la URL configurada)
        admin_url_path = get_admin_url_path()
        if not request.path.startswith(admin_url_path):
            return None
        
        # Obtener IP del cliente
        ip_address = self.get_client_ip(request)
        
        # 1. Verificar si la IP está bloqueada
        if self.is_ip_blocked(ip_address):
            logger.warning(
                f"Intento de acceso bloqueado desde IP: {ip_address} "
                f"a ruta: {request.path}",
                extra={
                    'ip': ip_address,
                    'path': request.path,
                    'user': request.user.username if request.user.is_authenticated else 'anonymous',
                }
            )
            return HttpResponseForbidden(
                "<h1>Acceso Denegado</h1>"
                "<p>Tu IP ha sido temporalmente bloqueada debido a múltiples "
                "intentos de acceso fallidos. Por favor, intenta más tarde.</p>",
                content_type='text/html'
            )
        
        # 2. Rate limiting para el admin
        if not self.check_rate_limit(ip_address):
            logger.warning(
                f"Rate limit excedido desde IP: {ip_address}",
                extra={
                    'ip': ip_address,
                    'path': request.path,
                }
            )
            return HttpResponse(
                "<h1>Demasiadas Solicitudes</h1>"
                "<p>Has excedido el límite de solicitudes. Por favor, espera un momento.</p>",
                status=429,
                content_type='text/html'
            )
        
        # 3. Logging de accesos al admin
        if request.user.is_authenticated and request.user.is_staff:
            logger.info(
                f"Acceso al admin desde IP: {ip_address} por usuario: {request.user.username}",
                extra={
                    'ip': ip_address,
                    'path': request.path,
                    'user': request.user.username,
                    'method': request.method,
                }
            )
        
        return None
    
    def process_response(self, request, response):
        """Procesa la respuesta después de que se genera"""
        
        # Solo aplicar a rutas del admin (usar la URL configurada)
        admin_url_path = get_admin_url_path()
        if not request.path.startswith(admin_url_path):
            return response
        
        # Detectar intentos de login fallidos
        # El admin de Django redirige a /login/ después de un login fallido
        if request.path.endswith('/login/') and request.method == 'POST':
            ip_address = self.get_client_ip(request)
            username = request.POST.get('username', 'unknown')
            
            # Si la respuesta es 200 (página de login), el login probablemente falló
            # Si es 302 (redirección), verificar si redirige de vuelta al login
            if response.status_code == 200 or (response.status_code == 302 and '/login/' in response.get('Location', '')):
                self.handle_failed_login(ip_address, request)
        
        return response
    
    def get_client_ip(self, request):
        """Obtiene la IP real del cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def is_ip_blocked(self, ip_address):
        """Verifica si una IP está bloqueada"""
        cache_key = f'admin_blocked_ip_{ip_address}'
        return cache.get(cache_key) is not None
    
    def block_ip(self, ip_address, duration=None):
        """Bloquea una IP por un período de tiempo"""
        if duration is None:
            duration = self.LOCKOUT_TIME
        
        cache_key = f'admin_blocked_ip_{ip_address}'
        cache.set(cache_key, True, duration)
        
        logger.warning(
            f"IP bloqueada: {ip_address} por {duration} segundos",
            extra={'ip': ip_address}
        )
    
    def handle_failed_login(self, ip_address, request):
        """Maneja un intento de login fallido"""
        attempt_key = f'admin_login_attempts_{ip_address}'
        attempts = cache.get(attempt_key, 0)
        attempts += 1
        
        logger.warning(
            f"Intento de login fallido #{attempts} desde IP: {ip_address}",
            extra={
                'ip': ip_address,
                'attempts': attempts,
                'username': request.POST.get('username', 'unknown'),
            }
        )
        
        # Si se excede el límite, bloquear la IP
        if attempts >= self.MAX_LOGIN_ATTEMPTS:
            self.block_ip(ip_address)
            cache.delete(attempt_key)  # Limpiar contador
        else:
            # Guardar intentos por 15 minutos
            cache.set(attempt_key, attempts, self.LOCKOUT_TIME)
    
    def check_rate_limit(self, ip_address):
        """Verifica el rate limit para una IP"""
        rate_key = f'admin_rate_limit_{ip_address}'
        requests = cache.get(rate_key, [])
        
        # Limpiar requests antiguos (fuera de la ventana de tiempo)
        now = time.time()
        requests = [req_time for req_time in requests if now - req_time < self.RATE_LIMIT_WINDOW]
        
        # Si se excede el límite, denegar
        if len(requests) >= self.RATE_LIMIT_REQUESTS:
            return False
        
        # Agregar el request actual
        requests.append(now)
        cache.set(rate_key, requests, self.RATE_LIMIT_WINDOW)
        
        return True


class AdminAccessLoggingMiddleware(MiddlewareMixin):
    """
    Middleware para registrar todos los accesos al admin
    """
    
    def process_request(self, request):
        """Registra el acceso al admin"""
        
        # Solo aplicar a rutas del admin (usar la URL configurada)
        admin_url_path = get_admin_url_path()
        if not request.path.startswith(admin_url_path):
            return None
        
        ip_address = self.get_client_ip(request)
        
        # Log detallado de accesos
        if request.user.is_authenticated:
            if request.user.is_staff:
                logger.info(
                    f"Admin access: {request.user.username} from {ip_address} to {request.path}",
                    extra={
                        'type': 'admin_access',
                        'user': request.user.username,
                        'ip': ip_address,
                        'path': request.path,
                        'method': request.method,
                        'timestamp': timezone.now().isoformat(),
                    }
                )
            else:
                logger.warning(
                    f"Intento de acceso al admin sin permisos: {request.user.username} from {ip_address}",
                    extra={
                        'type': 'unauthorized_admin_access',
                        'user': request.user.username,
                        'ip': ip_address,
                        'path': request.path,
                    }
                )
        else:
            # Intentos de acceso sin autenticación
            if request.path.endswith('/login/'):
                logger.info(
                    f"Intento de login al admin desde {ip_address}",
                    extra={
                        'type': 'admin_login_attempt',
                        'ip': ip_address,
                        'path': request.path,
                    }
                )
        
        return None
    
    def get_client_ip(self, request):
        """Obtiene la IP real del cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

