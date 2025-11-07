from django.utils import timezone
from django.contrib.auth import logout
from datetime import timedelta


class SessionTimeoutMiddleware:
    """
    Middleware para cerrar automáticamente la sesión de usuarios de gerencia
    después de 10 minutos de inactividad.
    """
    
    # Tiempo de inactividad en minutos
    TIMEOUT_MINUTES = 10
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Solo procesar si el usuario está autenticado
        if request.user.is_authenticated:
            # Solo aplicar a usuarios de gerencia
            if hasattr(request.user, 'rol') and request.user.rol == 'gerencia':
                # Obtener el tiempo de última actividad de la sesión
                last_activity = request.session.get('last_activity')
                
                if last_activity:
                    # Calcular el tiempo transcurrido desde la última actividad
                    last_activity_time = timezone.datetime.fromisoformat(last_activity)
                    if timezone.is_naive(last_activity_time):
                        last_activity_time = timezone.make_aware(last_activity_time)
                    
                    elapsed = timezone.now() - last_activity_time
                    
                    # Si han pasado más de 10 minutos, cerrar la sesión
                    if elapsed > timedelta(minutes=self.TIMEOUT_MINUTES):
                        # Limpiar la sesión
                        request.session.flush()
                        # Cerrar sesión del usuario
                        logout(request)
                        # Continuar con la respuesta (será redirigido al login)
                else:
                    # Si es la primera vez, establecer la última actividad
                    request.session['last_activity'] = timezone.now().isoformat()
                
                # Actualizar la última actividad en cada request
                if request.user.is_authenticated:  # Verificar nuevamente por si se cerró la sesión
                    request.session['last_activity'] = timezone.now().isoformat()
                    # Establecer el tiempo de expiración de la sesión
                    request.session.set_expiry(timedelta(minutes=self.TIMEOUT_MINUTES).total_seconds())
        
        response = self.get_response(request)
        return response

