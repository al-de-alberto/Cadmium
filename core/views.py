from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import IntegrityError
from django.db.models import Max
from .models import Usuario, Inventario, Asistencia, RegistroFalla, RegistroLlamada
from .forms import CrearUsuarioForm, RegistroAsistenciaForm, CambiarPasswordForm, EditarAsistenciaForm, EditarUsuarioForm, RegistroFallaForm, RegistroLlamadaForm


def login_view(request):
    """Vista para el login - siempre accesible"""
    # Si el usuario ya está autenticado, redirigir según su rol y estado
    if request.user.is_authenticated:
        # Solo usuarios trabajadores deben cambiar su contraseña
        if request.user.rol == 'usuario' and request.user.cambio_password_requerido:
            return redirect('cambiar_password')
        # Si es admin, ir al panel
        if request.user.es_administrador() or request.user.is_superuser:
            return redirect('panel')
        # Si es usuario trabajador sin necesidad de cambiar contraseña, redirigir a registro asistencia
        return redirect('registro_asistencia')
    
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
                
                # Solo usuarios trabajadores (rol='usuario') deben cambiar su contraseña
                if user.rol == 'usuario' and user.cambio_password_requerido:
                    return redirect('cambiar_password')
                
                # Verificar si hay un parámetro 'next' en la URL
                next_url = request.GET.get('next', None)
                if next_url:
                    return redirect(next_url)
                
                # Para administradores, ir al panel
                if user.es_administrador() or user.is_superuser:
                    return redirect('panel')
                
                # Para usuarios trabajadores, ir a registro asistencia
                if user.rol == 'usuario':
                    return redirect('registro_asistencia')
                
                # Fallback al panel
                return redirect('panel')
            else:
                # El tipo de cuenta no coincide con el rol del usuario
                messages.error(request, 'Usuario o Contraseña Incorrecto')
                return render(request, 'core/login.html', {'account_type': account_type})
        else:
            messages.error(request, 'Usuario o Contraseña Incorrecto')
            return render(request, 'core/login.html', {'account_type': account_type})
    
    return render(request, 'core/login.html')


def logout_view(request):
    """Vista para cerrar sesión - accesible sin autenticación para limpiar sesiones"""
    # Verificar si el usuario es administrador antes de cerrar sesión
    es_admin = request.user.is_authenticated and (request.user.es_administrador() or request.user.is_superuser)
    
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Sesión cerrada correctamente')
    
    # Si era administrador, redirigir al index, si no al login
    if es_admin:
        return redirect('index')
    return redirect('login')


@login_required
def cambiar_password_view(request):
    """Vista para cambiar la contraseña en el primer login (solo usuarios trabajadores)"""
    # Solo usuarios trabajadores pueden cambiar su contraseña aquí
    if request.user.rol != 'usuario':
        return redirect('panel')
    
    if not request.user.cambio_password_requerido:
        # Si el usuario ya cambió su contraseña, redirigir al panel
        return redirect('panel')
    
    form = CambiarPasswordForm(user=request.user)
    
    if request.method == 'POST':
        form = CambiarPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contraseña cambiada exitosamente. Por favor, inicie sesión nuevamente.')
            from django.contrib.auth import logout
            logout(request)
            return redirect('login')
    
    return render(request, 'core/cambiar_password.html', {'form': form})


@login_required
def panel_view(request):
    """Vista principal del panel de administrador"""
    # Solo usuarios trabajadores deben cambiar su contraseña
    if request.user.rol == 'usuario' and request.user.cambio_password_requerido:
        return redirect('cambiar_password')
    
    # Solo administradores pueden acceder al panel
    if not (request.user.es_administrador() or request.user.is_superuser):
        logout(request)
        return redirect('registro_asistencia')
    
    # Estadísticas generales
    stats = {
        'total_usuarios': Usuario.objects.count(),
    }
    
    return render(request, 'core/panel.html', {'stats': stats})


@login_required
def usuarios_view(request):
    """Vista para gestionar usuarios"""
    # Solo usuarios trabajadores deben cambiar su contraseña
    if request.user.rol == 'usuario' and request.user.cambio_password_requerido:
        return redirect('cambiar_password')
    if not (request.user.es_administrador() or request.user.is_superuser):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('panel')
    
    usuarios = Usuario.objects.all().order_by('-fecha_creacion')
    return render(request, 'core/usuarios.html', {'usuarios': usuarios})


@login_required
def crear_usuario_view(request):
    """Vista para crear usuarios desde el panel de administrador"""
    # Solo usuarios trabajadores deben cambiar su contraseña
    if request.user.rol == 'usuario' and request.user.cambio_password_requerido:
        return redirect('cambiar_password')
    if not (request.user.es_administrador() or request.user.is_superuser):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('panel')
    
    form = CrearUsuarioForm()
    
    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            try:
                usuario = form.save()
                messages.success(request, f'Usuario {usuario.get_nombre_completo()} creado exitosamente')
                return redirect('usuarios')
            except IntegrityError as e:
                messages.error(request, 'Error al crear el usuario. El RUT o correo ya existe.')
            except Exception as e:
                messages.error(request, f'Error al crear el usuario: {str(e)}')
    
    return render(request, 'core/crear_usuario.html', {'form': form})


@login_required
def editar_usuario_view(request, usuario_id):
    """Vista para editar un usuario desde el panel de administrador"""
    # Solo usuarios trabajadores deben cambiar su contraseña
    if request.user.rol == 'usuario' and request.user.cambio_password_requerido:
        return redirect('cambiar_password')
    if not (request.user.es_administrador() or request.user.is_superuser):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('panel')
    
    usuario = get_object_or_404(Usuario, id=usuario_id)
    
    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            try:
                usuario = form.save()
                messages.success(request, f'Usuario {usuario.get_nombre_completo()} actualizado exitosamente')
                return redirect('usuarios')
            except IntegrityError as e:
                messages.error(request, 'Error al actualizar el usuario. El RUT o correo ya existe.')
            except Exception as e:
                messages.error(request, f'Error al actualizar el usuario: {str(e)}')
    else:
        form = EditarUsuarioForm(instance=usuario)
    
    return render(request, 'core/editar_usuario.html', {'form': form, 'usuario': usuario})


@login_required
def inventario_view(request):
    """Vista para gestionar inventario"""
    # Solo usuarios trabajadores deben cambiar su contraseña
    if request.user.rol == 'usuario' and request.user.cambio_password_requerido:
        return redirect('cambiar_password')
    if not (request.user.es_administrador() or request.user.is_superuser):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('panel')
    
    inventarios = Inventario.objects.all().order_by('-fecha_actualizacion')
    return render(request, 'core/inventario.html', {'inventarios': inventarios})


@login_required
def ventas_pedidos_view(request):
    """Vista para gestionar ventas y pedidos"""
    # Solo usuarios trabajadores deben cambiar su contraseña
    if request.user.rol == 'usuario' and request.user.cambio_password_requerido:
        return redirect('cambiar_password')
    if not (request.user.es_administrador() or request.user.is_superuser):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('panel')
    
    # Por ahora, renderizar una página básica
    return render(request, 'core/ventas_pedidos.html')


@login_required
def deliverys_view(request):
    """Vista para gestionar deliverys"""
    # Solo usuarios trabajadores deben cambiar su contraseña
    if request.user.rol == 'usuario' and request.user.cambio_password_requerido:
        return redirect('cambiar_password')
    if not (request.user.es_administrador() or request.user.is_superuser):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('panel')
    
    # Por ahora, renderizar una página básica
    return render(request, 'core/deliverys.html')


@login_required
def operaciones_view(request):
    """Vista para gestionar operaciones"""
    # Solo usuarios trabajadores deben cambiar su contraseña
    if request.user.rol == 'usuario' and request.user.cambio_password_requerido:
        return redirect('cambiar_password')
    if not (request.user.es_administrador() or request.user.is_superuser):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('panel')
    
    from datetime import datetime, timedelta
    from django.db.models import Count, Avg
    
    # Obtener registros de fallas y llamadas
    fallas = RegistroFalla.objects.all().order_by('-fecha', '-contador_falla')
    llamadas = RegistroLlamada.objects.all().order_by('-fecha', '-contador_llamada')
    
    # Calcular porcentajes mensuales
    fecha_actual = timezone.localtime(timezone.now())
    inicio_mes = fecha_actual.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Calcular días transcurridos del mes actual
    dias_transcurridos = fecha_actual.day
    
    # Fallas del mes actual
    fallas_mes = RegistroFalla.objects.filter(fecha__gte=inicio_mes)
    total_fallas_mes = fallas_mes.count()
    
    # Calcular días únicos con fallas
    dias_con_fallas = fallas_mes.values('fecha').distinct().count()
    porcentaje_fallas_mes = round((dias_con_fallas / dias_transcurridos * 100), 1) if dias_transcurridos > 0 else 0
    
    # Llamadas del mes actual
    llamadas_mes = RegistroLlamada.objects.filter(fecha__gte=inicio_mes)
    total_llamadas_mes = llamadas_mes.count()
    
    # Calcular días únicos con llamadas
    dias_con_llamadas = llamadas_mes.values('fecha').distinct().count()
    porcentaje_llamadas_mes = round((dias_con_llamadas / dias_transcurridos * 100), 1) if dias_transcurridos > 0 else 0
    
    # Obtener siguiente contador para fallas y llamadas
    siguiente_contador_falla = (RegistroFalla.objects.aggregate(Max('contador_falla'))['contador_falla__max'] or 0) + 1
    siguiente_contador_llamada = (RegistroLlamada.objects.aggregate(Max('contador_llamada'))['contador_llamada__max'] or 0) + 1
    
    return render(request, 'core/operaciones.html', {
        'fallas': fallas[:10],  # Últimas 10 fallas
        'llamadas': llamadas[:10],  # Últimas 10 llamadas
        'total_fallas_mes': total_fallas_mes,
        'total_llamadas_mes': total_llamadas_mes,
        'porcentaje_fallas_mes': porcentaje_fallas_mes,
        'porcentaje_llamadas_mes': porcentaje_llamadas_mes,
        'siguiente_contador_falla': siguiente_contador_falla,
        'siguiente_contador_llamada': siguiente_contador_llamada,
    })


@login_required
def crear_falla_view(request):
    """Vista para crear un nuevo registro de falla"""
    if request.user.rol == 'usuario' and request.user.cambio_password_requerido:
        return redirect('cambiar_password')
    if not (request.user.es_administrador() or request.user.is_superuser):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('panel')
    
    from django.db.models import Max
    
    if request.method == 'POST':
        form = RegistroFallaForm(request.POST)
        if form.is_valid():
            falla = form.save(commit=False)
            # Asignar contador automáticamente
            ultimo_contador = RegistroFalla.objects.aggregate(Max('contador_falla'))['contador_falla__max']
            falla.contador_falla = (ultimo_contador or 0) + 1
            falla.usuario_registro = request.user
            falla.save()
            messages.success(request, f'Falla #{falla.contador_falla} registrada exitosamente.')
            return redirect('operaciones')
    else:
        form = RegistroFallaForm()
    
    return render(request, 'core/crear_falla.html', {'form': form})


@login_required
def crear_llamada_view(request):
    """Vista para crear un nuevo registro de llamada"""
    if request.user.rol == 'usuario' and request.user.cambio_password_requerido:
        return redirect('cambiar_password')
    if not (request.user.es_administrador() or request.user.is_superuser):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('panel')
    
    from django.db.models import Max
    
    if request.method == 'POST':
        form = RegistroLlamadaForm(request.POST)
        if form.is_valid():
            llamada = form.save(commit=False)
            # Asignar contador automáticamente
            ultimo_contador = RegistroLlamada.objects.aggregate(Max('contador_llamada'))['contador_llamada__max']
            llamada.contador_llamada = (ultimo_contador or 0) + 1
            llamada.usuario_registro = request.user
            llamada.save()
            messages.success(request, f'Llamada #{llamada.contador_llamada} registrada exitosamente.')
            return redirect('operaciones')
    else:
        form = RegistroLlamadaForm()
    
    return render(request, 'core/crear_llamada.html', {'form': form})


@login_required
def editar_falla_view(request, falla_id):
    """Vista para editar un registro de falla"""
    if request.user.rol == 'usuario' and request.user.cambio_password_requerido:
        return redirect('cambiar_password')
    if not (request.user.es_administrador() or request.user.is_superuser):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('panel')
    
    falla = get_object_or_404(RegistroFalla, id=falla_id)
    
    if request.method == 'POST':
        form = RegistroFallaForm(request.POST, instance=falla)
        if form.is_valid():
            form.save()
            messages.success(request, f'Falla #{falla.contador_falla} actualizada exitosamente.')
            return redirect('operaciones')
    else:
        form = RegistroFallaForm(instance=falla)
    
    return render(request, 'core/editar_falla.html', {'form': form, 'falla': falla})


@login_required
def eliminar_falla_view(request, falla_id):
    """Vista para eliminar un registro de falla"""
    if request.user.rol == 'usuario' and request.user.cambio_password_requerido:
        return redirect('cambiar_password')
    if not (request.user.es_administrador() or request.user.is_superuser):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('panel')
    
    falla = get_object_or_404(RegistroFalla, id=falla_id)
    
    if request.method == 'POST':
        contador = falla.contador_falla
        falla.delete()
        messages.success(request, f'Falla #{contador} eliminada exitosamente.')
        return redirect('operaciones')
    
    return render(request, 'core/eliminar_falla.html', {'falla': falla})


@login_required
def editar_llamada_view(request, llamada_id):
    """Vista para editar un registro de llamada"""
    if request.user.rol == 'usuario' and request.user.cambio_password_requerido:
        return redirect('cambiar_password')
    if not (request.user.es_administrador() or request.user.is_superuser):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('panel')
    
    llamada = get_object_or_404(RegistroLlamada, id=llamada_id)
    
    if request.method == 'POST':
        form = RegistroLlamadaForm(request.POST, instance=llamada)
        if form.is_valid():
            form.save()
            messages.success(request, f'Llamada #{llamada.contador_llamada} actualizada exitosamente.')
            return redirect('operaciones')
    else:
        form = RegistroLlamadaForm(instance=llamada)
    
    return render(request, 'core/editar_llamada.html', {'form': form, 'llamada': llamada})


@login_required
def eliminar_llamada_view(request, llamada_id):
    """Vista para eliminar un registro de llamada"""
    if request.user.rol == 'usuario' and request.user.cambio_password_requerido:
        return redirect('cambiar_password')
    if not (request.user.es_administrador() or request.user.is_superuser):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('panel')
    
    llamada = get_object_or_404(RegistroLlamada, id=llamada_id)
    
    if request.method == 'POST':
        contador = llamada.contador_llamada
        llamada.delete()
        messages.success(request, f'Llamada #{contador} eliminada exitosamente.')
        return redirect('operaciones')
    
    return render(request, 'core/eliminar_llamada.html', {'llamada': llamada})


@login_required
def asistencia_view(request):
    """Vista para gestionar asistencia"""
    # Solo usuarios trabajadores deben cambiar su contraseña
    if request.user.rol == 'usuario' and request.user.cambio_password_requerido:
        return redirect('cambiar_password')
    if not (request.user.es_administrador() or request.user.is_superuser):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('panel')
    
    from django.db.models import Q
    from datetime import datetime, timedelta
    
    # Obtener parámetros de filtrado
    busqueda = request.GET.get('busqueda', '').strip()
    orden = request.GET.get('orden', 'desc')  # 'asc' o 'desc'
    filtro_fecha = request.GET.get('filtro_fecha', '')  # 'hoy', 'semana', 'mes', 'todos'
    filtro_turno = request.GET.get('filtro_turno', '')  # 'apertura', 'tarde', 'cierre', ''
    
    # Iniciar con todas las asistencias
    asistencias = Asistencia.objects.select_related('usuario').all()
    
    # Aplicar búsqueda por nombre (coincidencias parciales)
    if busqueda:
        # Buscar en nombre, apellido, nombre completo y username
        # El operador icontains busca coincidencias parciales sin distinguir mayúsculas/minúsculas
        asistencias = asistencias.filter(
            Q(usuario__nombre__icontains=busqueda) |
            Q(usuario__apellido__icontains=busqueda) |
            Q(usuario__username__icontains=busqueda)
        )
    
    # Aplicar filtro por fecha
    fecha_actual = timezone.localtime(timezone.now()).date()
    if filtro_fecha == 'hoy':
        asistencias = asistencias.filter(fecha=fecha_actual)
    elif filtro_fecha == 'semana':
        fecha_inicio = fecha_actual - timedelta(days=7)
        asistencias = asistencias.filter(fecha__gte=fecha_inicio)
    elif filtro_fecha == 'mes':
        fecha_inicio = fecha_actual - timedelta(days=30)
        asistencias = asistencias.filter(fecha__gte=fecha_inicio)
    # Si es 'todos' o vacío, no se filtra por fecha
    
    # Aplicar filtro por turno
    if filtro_turno:
        asistencias = asistencias.filter(turno=filtro_turno)
    
    # Aplicar ordenamiento
    if orden == 'asc':
        asistencias = asistencias.order_by('fecha', 'fecha_registro')
    else:  # desc (por defecto)
        asistencias = asistencias.order_by('-fecha', '-fecha_registro')
    
    # Calcular usuario con mayor y menor asistencia
    from django.db.models import Count
    usuarios_asistencias = Usuario.objects.annotate(
        total_asistencias=Count('asistencias')
    ).filter(total_asistencias__gt=0).order_by('-total_asistencias')
    
    usuario_mayor_asistencia = usuarios_asistencias.first() if usuarios_asistencias.exists() else None
    usuario_menor_asistencia = usuarios_asistencias.last() if usuarios_asistencias.exists() else None
    
    # Si hay solo un usuario, no hay menor (es el mismo)
    if usuarios_asistencias.count() == 1:
        usuario_menor_asistencia = None
    
    return render(request, 'core/asistencia.html', {
        'asistencias': asistencias,
        'busqueda': busqueda,
        'orden': orden,
        'filtro_fecha': filtro_fecha,
        'filtro_turno': filtro_turno,
        'usuario_mayor_asistencia': usuario_mayor_asistencia,
        'usuario_menor_asistencia': usuario_menor_asistencia,
    })


@login_required
def editar_asistencia_view(request, asistencia_id):
    """Vista para editar un registro de asistencia"""
    # Solo usuarios trabajadores deben cambiar su contraseña
    if request.user.rol == 'usuario' and request.user.cambio_password_requerido:
        return redirect('cambiar_password')
    if not (request.user.es_administrador() or request.user.is_superuser):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('panel')
    
    asistencia = get_object_or_404(Asistencia, id=asistencia_id)
    
    if request.method == 'POST':
        form = EditarAsistenciaForm(request.POST, instance=asistencia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro de asistencia actualizado exitosamente.')
            return redirect('asistencia')
    else:
        form = EditarAsistenciaForm(instance=asistencia)
    
    return render(request, 'core/editar_asistencia.html', {'form': form, 'asistencia': asistencia})


@login_required
def eliminar_asistencia_view(request, asistencia_id):
    """Vista para eliminar un registro de asistencia"""
    # Solo usuarios trabajadores deben cambiar su contraseña
    if request.user.rol == 'usuario' and request.user.cambio_password_requerido:
        return redirect('cambiar_password')
    if not (request.user.es_administrador() or request.user.is_superuser):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('panel')
    
    asistencia = get_object_or_404(Asistencia, id=asistencia_id)
    
    if request.method == 'POST':
        usuario_nombre = asistencia.usuario.nombre or asistencia.usuario.username
        asistencia.delete()
        messages.success(request, f'Registro de asistencia de {usuario_nombre} eliminado exitosamente.')
        return redirect('asistencia')
    
    return render(request, 'core/eliminar_asistencia.html', {'asistencia': asistencia})


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


@login_required
def registro_asistencia_view(request):
    """Vista para registro de asistencia (solo usuarios trabajadores)"""
    # Solo usuarios trabajadores pueden registrar asistencia
    if request.user.rol != 'usuario':
        messages.error(request, 'Solo los usuarios trabajadores pueden registrar asistencia')
        return redirect('panel')
    
    # Si el usuario necesita cambiar su contraseña, redirigir primero
    if request.user.cambio_password_requerido:
        return redirect('cambiar_password')
    
    form = RegistroAsistenciaForm()
    
    if request.method == 'POST':
        form = RegistroAsistenciaForm(request.POST)
        if form.is_valid():
            turno = form.cleaned_data['turno']
            
            # Obtener el usuario logueado
            usuario = request.user
            
            # Mapear turno a horas de entrada y salida (horario chileno GMT-3)
            horarios_turno = {
                'apertura': {'entrada': '09:00', 'salida': '13:00'},
                'tarde': {'entrada': '13:00', 'salida': '17:00'},
                'cierre': {'entrada': '17:00', 'salida': '21:00'}
            }
            horario = horarios_turno.get(turno, {'entrada': '09:00', 'salida': '13:00'})
            from datetime import datetime
            hora_entrada = datetime.strptime(horario['entrada'], '%H:%M').time()
            hora_salida = datetime.strptime(horario['salida'], '%H:%M').time()
            
            try:
                # Verificar si ya existe asistencia para hoy (usando zona horaria de Chile GMT-3)
                fecha_hoy = timezone.localtime(timezone.now()).date()
                asistencia_existente = Asistencia.objects.filter(
                    usuario=usuario,
                    fecha=fecha_hoy
                ).first()
                
                if asistencia_existente:
                    messages.warning(request, f'Ya se registró asistencia para hoy. Tu turno registrado es: {asistencia_existente.get_turno_display()}')
                    # Cerrar sesión y redirigir al index
                    logout(request)
                    return redirect('index')
                else:
                    # Crear nuevo registro de asistencia
                    # fecha_registro se guarda automáticamente con la fecha y hora exacta del registro (GMT-3 Chile)
                    fecha_registro_chile = timezone.localtime(timezone.now())
                    asistencia = Asistencia.objects.create(
                        usuario=usuario,
                        fecha=fecha_hoy,
                        hora_entrada=hora_entrada,
                        hora_salida=hora_salida,
                        estado='presente',
                        turno=turno,
                        fecha_registro=fecha_registro_chile  # Fecha y hora exacta del registro en horario chileno GMT-3
                    )
                    messages.success(request, f'Asistencia registrada exitosamente. Turno: {asistencia.get_turno_display()}')
                    # Cerrar sesión y redirigir al index
                    logout(request)
                    return redirect('index')
                
            except Exception as e:
                messages.error(request, f'Error al registrar asistencia: {str(e)}')
                import traceback
                print(traceback.format_exc())  # Para debugging
    
    # Obtener la fecha actual para mostrar en el template (horario chileno GMT-3)
    fecha_actual = timezone.localtime(timezone.now()).date()
    return render(request, 'core/registro_asistencia.html', {
        'form': form, 
        'usuario': request.user,
        'fecha_actual': fecha_actual
    })

