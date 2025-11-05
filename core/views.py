from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Usuario, Inventario, Asistencia


def login_view(request):
    """Vista para el login"""
    if request.user.is_authenticated:
        return redirect('panel')
    
    if request.method == 'POST':
        account_type = request.POST.get('account_type')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Validar que se haya seleccionado un tipo de cuenta
        if not account_type:
            messages.error(request, 'Por favor selecciona un tipo de cuenta')
            return render(request, 'core/login.html')
        
        # Validar que se hayan proporcionado credenciales
        if not username or not password:
            messages.error(request, 'Por favor completa todos los campos')
            return render(request, 'core/login.html', {'account_type': account_type})
        
        # Autenticar usuario
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Validar que el tipo de cuenta seleccionado coincida con el rol del usuario
            expected_rol = 'admin' if account_type == 'gerencia' else 'usuario'
            
            if user.rol == expected_rol or (account_type == 'gerencia' and user.is_superuser):
                login(request, user)
                return redirect('panel')
            else:
                # El tipo de cuenta no coincide con el rol del usuario
                messages.error(request, 'Usuario o Contraseña Incorrecto')
                return render(request, 'core/login.html', {'account_type': account_type})
        else:
            messages.error(request, 'Usuario o Contraseña Incorrecto')
            return render(request, 'core/login.html', {'account_type': account_type})
    
    return render(request, 'core/login.html')


@login_required
def logout_view(request):
    """Vista para cerrar sesión"""
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente')
    return redirect('login')


@login_required
def panel_view(request):
    """Vista principal del panel de administrador"""
    # Solo administradores pueden acceder
    if not (request.user.es_administrador() or request.user.is_superuser):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('login')
    
    # Estadísticas generales
    stats = {
        'total_usuarios': Usuario.objects.count(),
        'total_inventario': Inventario.objects.count(),
        'total_asistencias': Asistencia.objects.count(),
        'asistencias_hoy': Asistencia.objects.filter(fecha=timezone.now().date()).count(),
    }
    
    return render(request, 'core/panel.html', {'stats': stats})


@login_required
def usuarios_view(request):
    """Vista para gestionar usuarios"""
    if not (request.user.es_administrador() or request.user.is_superuser):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('panel')
    
    usuarios = Usuario.objects.all().order_by('-fecha_creacion')
    return render(request, 'core/usuarios.html', {'usuarios': usuarios})


@login_required
def inventario_view(request):
    """Vista para gestionar inventario"""
    if not (request.user.es_administrador() or request.user.is_superuser):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('panel')
    
    inventarios = Inventario.objects.all().order_by('-fecha_actualizacion')
    return render(request, 'core/inventario.html', {'inventarios': inventarios})


@login_required
def asistencia_view(request):
    """Vista para gestionar asistencia"""
    if not (request.user.es_administrador() or request.user.is_superuser):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('panel')
    
    asistencias = Asistencia.objects.select_related('usuario').all().order_by('-fecha', '-fecha_registro')
    return render(request, 'core/asistencia.html', {'asistencias': asistencias})


def index_view(request):
    """Vista para la página principal"""
    return render(request, 'core/index.html')


def contactanos_view(request):
    """Vista para la página de contáctanos"""
    # Lista de contactos de gerencia (5 contactos)
    contactos = [
        {
            'nombre': 'Gerente General',
            'cargo': 'Gerente General',
            'email': 'gerente.general@popupnescafe.cl',
            'telefono': '+56 9 XXXX XXXX',
        },
        {
            'nombre': 'Gerente de Operaciones',
            'cargo': 'Gerente de Operaciones',
            'email': 'operaciones@popupnescafe.cl',
            'telefono': '+56 9 XXXX XXXX',
        },
        {
            'nombre': 'Gerente de Recursos Humanos',
            'cargo': 'Gerente de RRHH',
            'email': 'rrhh@popupnescafe.cl',
            'telefono': '+56 9 XXXX XXXX',
        },
        {
            'nombre': 'Gerente Comercial',
            'cargo': 'Gerente Comercial',
            'email': 'comercial@popupnescafe.cl',
            'telefono': '+56 9 XXXX XXXX',
        },
        {
            'nombre': 'Gerente Administrativo',
            'cargo': 'Gerente Administrativo',
            'email': 'administracion@popupnescafe.cl',
            'telefono': '+56 9 XXXX XXXX',
        },
    ]
    return render(request, 'core/contactanos.html', {'contactos': contactos})

