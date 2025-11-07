from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import IntegrityError
from django.db.models import Max, Q
from .models import Usuario, Inventario, Asistencia, RegistroFalla, RegistroLlamada, Pedido, DetallePedido, Auditoria
from .forms import CrearUsuarioForm, RegistroAsistenciaForm, CambiarPasswordForm, EditarAsistenciaForm, EditarUsuarioForm, RegistroFallaForm, RegistroLlamadaForm, CrearInventarioForm, EditarInventarioForm, CrearPedidoForm, CambiarStockForm
from django.http import HttpResponse
import json


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
        # Si es usuario trabajador sin necesidad de cambiar contraseña, redirigir a dashboard trabajador
        return redirect('trabajador_dashboard')
    
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
            # Verificar si el usuario está activo
            if not user.activo:
                messages.error(request, 'Tu cuenta está inactiva. Contacta al administrador para más información.')
                return render(request, 'core/login.html', {'account_type': account_type})
            
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
                
                # Para usuarios trabajadores, ir a dashboard trabajador
                if user.rol == 'usuario':
                    return redirect('trabajador_dashboard')
                
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
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Sesión cerrada correctamente')
    
    # Siempre redirigir al index después de cerrar sesión
    return redirect('index')


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
            return redirect('index')
    
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
    
    # Verificar si el usuario intenta cambiar su propio estado y es administrador
    es_propia_cuenta_admin = usuario.id == request.user.id and (usuario.es_administrador() or usuario.is_superuser)
    
    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            try:
                # Guardar datos anteriores para auditoría
                datos_anteriores = {
                    'nombre': usuario.nombre,
                    'apellido': usuario.apellido,
                    'rut': usuario.rut,
                    'correo_institucional': usuario.correo_institucional,
                    'rol': usuario.rol,
                    'activo': usuario.activo,
                }
                
                # Si es su propia cuenta de administrador, prevenir cambio de estado activo
                if es_propia_cuenta_admin:
                    # Restaurar el estado activo a True antes de guardar
                    usuario = form.save(commit=False)
                    usuario.activo = True
                    usuario.save()
                    messages.info(request, 'No puedes desactivar tu propia cuenta de administrador. El estado activo se mantuvo en True.')
                else:
                    usuario = form.save()
                # Registrar auditoría
                from .utils import registrar_auditoria
                detalles = {
                    'datos_anteriores': datos_anteriores,
                    'datos_nuevos': {
                        'nombre': usuario.nombre,
                        'apellido': usuario.apellido,
                        'rut': usuario.rut,
                        'correo_institucional': usuario.correo_institucional,
                        'rol': usuario.rol,
                        'activo': usuario.activo,
                    }
                }
                registrar_auditoria(
                    usuario=request.user,
                    accion='usuario_edit',
                    modulo='usuarios',
                    descripcion=f'Usuario "{usuario.get_nombre_completo()}" (username: {usuario.username}) modificado',
                    objeto_afectado=f"{usuario.nombre} {usuario.apellido}",
                    detalles=detalles
                )
                messages.success(request, f'Usuario {usuario.get_nombre_completo()} actualizado exitosamente')
                return redirect('usuarios')
            except IntegrityError as e:
                messages.error(request, 'Error al actualizar el usuario. El RUT o correo ya existe.')
            except Exception as e:
                messages.error(request, f'Error al actualizar el usuario: {str(e)}')
    else:
        form = EditarUsuarioForm(instance=usuario)
        # Si es su propia cuenta de administrador, deshabilitar el campo activo
        if es_propia_cuenta_admin:
            form.fields['activo'].widget.attrs['disabled'] = True
            form.fields['activo'].widget.attrs['readonly'] = True
    
    return render(request, 'core/editar_usuario.html', {
        'form': form, 
        'usuario': usuario,
        'es_propia_cuenta_admin': es_propia_cuenta_admin
    })


@login_required
def eliminar_usuario_view(request, usuario_id):
    """Vista para eliminar un usuario (solo si no tiene registros relacionados)"""
    # Solo usuarios trabajadores deben cambiar su contraseña
    if request.user.rol == 'usuario' and request.user.cambio_password_requerido:
        return redirect('cambiar_password')
    if not (request.user.es_administrador() or request.user.is_superuser):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('panel')
    
    usuario = get_object_or_404(Usuario, id=usuario_id)
    
    # Verificar si el usuario intenta eliminar/desactivar su propia cuenta y es administrador
    if usuario.id == request.user.id and (usuario.es_administrador() or usuario.is_superuser):
        messages.error(request, 'No puedes eliminar o desactivar tu propia cuenta de administrador.')
        return redirect('usuarios')
    
    # Verificar si el usuario tiene registros relacionados
    tiene_asistencias = usuario.asistencias.exists()
    tiene_fallas = usuario.fallas_registradas.exists()
    tiene_llamadas = usuario.llamadas_registradas.exists()
    tiene_pedidos = usuario.pedidos_creados.exists()
    tiene_auditorias = usuario.auditorias.exists()
    
    tiene_registros = tiene_asistencias or tiene_fallas or tiene_llamadas or tiene_pedidos or tiene_auditorias
    
    if request.method == 'POST':
        if tiene_registros:
            # Solo desactivar si tiene registros
            usuario.activo = False
            usuario.save()
            # Registrar auditoría
            from .utils import registrar_auditoria
            registrar_auditoria(
                usuario=request.user,
                accion='usuario_deactivate',
                modulo='usuarios',
                descripcion=f'Usuario "{usuario.get_nombre_completo()}" desactivado (tiene registros relacionados)',
                objeto_afectado=f"{usuario.nombre} {usuario.apellido}",
                detalles={
                    'tiene_asistencias': tiene_asistencias,
                    'tiene_fallas': tiene_fallas,
                    'tiene_llamadas': tiene_llamadas,
                    'tiene_pedidos': tiene_pedidos,
                    'tiene_auditorias': tiene_auditorias,
                }
            )
            messages.warning(request, f'El usuario {usuario.get_nombre_completo()} tiene registros relacionados. Se ha desactivado en lugar de eliminar.')
            return redirect('usuarios')
        else:
            # Eliminar si no tiene registros
            nombre_completo = usuario.get_nombre_completo()
            usuario_nombre = f"{usuario.nombre} {usuario.apellido}"
            # Registrar auditoría antes de eliminar
            from .utils import registrar_auditoria
            registrar_auditoria(
                usuario=request.user,
                accion='usuario_delete',
                modulo='usuarios',
                descripcion=f'Usuario "{nombre_completo}" eliminado',
                objeto_afectado=usuario_nombre,
                detalles={
                    'username': usuario.username,
                    'rut': usuario.rut,
                    'correo_institucional': usuario.correo_institucional,
                }
            )
            usuario.delete()
            messages.success(request, f'Usuario {nombre_completo} eliminado exitosamente.')
            return redirect('usuarios')
    
    # Preparar información sobre los registros
    registros_info = []
    if tiene_asistencias:
        count = usuario.asistencias.count()
        registros_info.append(f'{count} registro(s) de asistencia')
    if tiene_fallas:
        count = usuario.fallas_registradas.count()
        registros_info.append(f'{count} registro(s) de fallas')
    if tiene_llamadas:
        count = usuario.llamadas_registradas.count()
        registros_info.append(f'{count} registro(s) de llamadas')
    if tiene_pedidos:
        count = usuario.pedidos_creados.count()
        registros_info.append(f'{count} pedido(s)')
    if tiene_auditorias:
        count = usuario.auditorias.count()
        registros_info.append(f'{count} registro(s) de auditoría')
    
    return render(request, 'core/eliminar_usuario.html', {
        'usuario': usuario,
        'tiene_registros': tiene_registros,
        'registros_info': registros_info
    })


@login_required
def inventario_view(request):
    """Vista para gestionar inventario"""
    # Solo usuarios trabajadores deben cambiar su contraseña
    if request.user.rol == 'usuario' and request.user.cambio_password_requerido:
        return redirect('cambiar_password')
    if not (request.user.es_administrador() or request.user.is_superuser):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('panel')
    
    # Organizar productos por categoría
    bodega = Inventario.objects.filter(categoria='bodega').order_by('nombre')
    meson = Inventario.objects.filter(categoria='meson').order_by('nombre')
    limpieza = Inventario.objects.filter(categoria='limpieza').order_by('nombre')
    
    context = {
        'bodega': bodega,
        'meson': meson,
        'limpieza': limpieza,
    }
    
    return render(request, 'core/inventario.html', context)


@login_required
def crear_inventario_view(request):
    """Vista para crear productos de inventario"""
    if request.user.rol == 'usuario' and request.user.cambio_password_requerido:
        return redirect('cambiar_password')
    if not (request.user.es_administrador() or request.user.is_superuser):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('panel')
    
    form = CrearInventarioForm()
    
    if request.method == 'POST':
        form = CrearInventarioForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                producto = form.save()
                messages.success(request, f'Producto "{producto.nombre}" creado exitosamente.')
                return redirect('inventario')
            except Exception as e:
                messages.error(request, f'Error al crear el producto: {str(e)}')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    
    return render(request, 'core/crear_inventario.html', {'form': form})


@login_required
def editar_inventario_view(request, producto_id):
    """Vista para editar un producto de inventario"""
    if request.user.rol == 'usuario' and request.user.cambio_password_requerido:
        return redirect('cambiar_password')
    if not (request.user.es_administrador() or request.user.is_superuser):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('panel')
    
    try:
        producto = Inventario.objects.get(id=producto_id)
    except Inventario.DoesNotExist:
        messages.error(request, "El producto no existe.")
        return redirect('inventario')
    
    if request.method == 'POST':
        form = EditarInventarioForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            # Guardar datos anteriores para auditoría
            datos_anteriores = {
                'nombre': producto.nombre,
                'categoria': producto.categoria,
                'cantidad': producto.cantidad,
            }
            form.save()
            producto.refresh_from_db()
            # Registrar auditoría
            from .utils import registrar_auditoria
            detalles = {
                'datos_anteriores': datos_anteriores,
                'datos_nuevos': {
                    'nombre': producto.nombre,
                    'categoria': producto.categoria,
                    'cantidad': producto.cantidad,
                }
            }
            registrar_auditoria(
                usuario=request.user,
                accion='inventario_edit',
                modulo='inventario',
                descripcion=f'Producto "{producto.nombre}" modificado',
                objeto_afectado=producto.nombre,
                detalles=detalles
            )
            messages.success(request, f'Producto "{producto.nombre}" actualizado correctamente.')
            return redirect('inventario')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = EditarInventarioForm(instance=producto)
    
    return render(request, 'core/editar_inventario.html', {
        'form': form,
        'producto': producto
    })


@login_required
def eliminar_inventario_view(request, producto_id):
    """Vista para eliminar un producto de inventario"""
    if request.user.rol == 'usuario' and request.user.cambio_password_requerido:
        return redirect('cambiar_password')
    if not (request.user.es_administrador() or request.user.is_superuser):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('panel')
    
    try:
        producto = Inventario.objects.get(id=producto_id)
    except Inventario.DoesNotExist:
        messages.error(request, "El producto no existe.")
        return redirect('inventario')
    
    if request.method == 'POST':
        nombre_producto = producto.nombre
        categoria_producto = producto.categoria
        cantidad_producto = producto.cantidad
        # Registrar auditoría antes de eliminar
        from .utils import registrar_auditoria
        registrar_auditoria(
            usuario=request.user,
            accion='inventario_delete',
            modulo='inventario',
            descripcion=f'Producto "{nombre_producto}" eliminado',
            objeto_afectado=nombre_producto,
            detalles={
                'categoria': categoria_producto,
                'cantidad': cantidad_producto,
            }
        )
        # Eliminar la imagen si existe
        if producto.imagen:
            producto.imagen.delete()
        producto.delete()
        messages.success(request, f'Producto "{nombre_producto}" eliminado exitosamente.')
        return redirect('inventario')
    
    return render(request, 'core/eliminar_inventario.html', {'producto': producto})


@login_required
def ventas_pedidos_view(request):
    """Vista para gestionar ventas y pedidos"""
    # Solo usuarios trabajadores deben cambiar su contraseña
    if request.user.rol == 'usuario' and request.user.cambio_password_requerido:
        return redirect('cambiar_password')
    if not (request.user.es_administrador() or request.user.is_superuser):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('panel')
    
    pedidos = Pedido.objects.all().order_by('-fecha_creacion')
    return render(request, 'core/ventas_pedidos.html', {'pedidos': pedidos})


@login_required
def crear_pedido_view(request):
    """Vista para crear un nuevo pedido"""
    if request.user.rol == 'usuario' and request.user.cambio_password_requerido:
        return redirect('cambiar_password')
    if not (request.user.es_administrador() or request.user.is_superuser):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('panel')
    
    if request.method == 'POST':
        form = CrearPedidoForm(request.POST)
        productos_data = json.loads(request.POST.get('productos', '[]'))
        
        if form.is_valid() and productos_data:
            pedido = form.save(commit=False)
            pedido.usuario_creacion = request.user
            pedido.save()
            
            # Crear los detalles del pedido
            for producto in productos_data:
                DetallePedido.objects.create(
                    pedido=pedido,
                    producto_nombre=producto.get('nombre', ''),
                    cantidad=producto.get('cantidad', 0)
                )
            
            messages.success(request, f'Pedido "{pedido.nombre}" creado exitosamente.')
            return redirect('ventas_pedidos')
        else:
            if not productos_data:
                messages.error(request, 'Debe agregar al menos un producto al pedido.')
    else:
        form = CrearPedidoForm()
    
    return render(request, 'core/crear_pedido.html', {'form': form})


@login_required
def exportar_pedido_excel(request, pedido_id):
    """Vista para exportar un pedido a Excel"""
    if request.user.rol == 'usuario' and request.user.cambio_password_requerido:
        return redirect('cambiar_password')
    if not (request.user.es_administrador() or request.user.is_superuser):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('panel')
    
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, Alignment, PatternFill
    except ImportError:
        messages.error(request, 'La librería openpyxl no está instalada.')
        return redirect('ventas_pedidos')
    
    pedido = get_object_or_404(Pedido, id=pedido_id)
    detalles = pedido.detalles.all()
    
    # Crear un libro de trabajo Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Pedido"
    
    # Estilos
    header_fill = PatternFill(start_color="B08968", end_color="B08968", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=12)
    title_font = Font(bold=True, size=14)
    
    # Encabezado
    ws['A1'] = "PEDIDO"
    ws['A1'].font = title_font
    ws.merge_cells('A1:C1')
    
    ws['A2'] = f"Nombre: {pedido.nombre}"
    ws['A3'] = f"Fecha: {pedido.fecha_creacion.strftime('%d/%m/%Y %H:%M')}"
    ws['A4'] = f"Usuario: {pedido.usuario_creacion.get_nombre_completo() if pedido.usuario_creacion else 'N/A'}"
    
    if pedido.observaciones:
        ws['A5'] = f"Observaciones: {pedido.observaciones}"
    
    # Encabezados de tabla
    ws['A7'] = "Nombre del Producto"
    ws['B7'] = "Cantidad"
    ws['C7'] = "Total"
    
    for cell in ['A7', 'B7', 'C7']:
        ws[cell].fill = header_fill
        ws[cell].font = header_font
        ws[cell].alignment = Alignment(horizontal='center', vertical='center')
    
    # Datos
    row = 8
    for detalle in detalles:
        ws[f'A{row}'] = detalle.producto_nombre
        ws[f'B{row}'] = detalle.cantidad
        ws[f'C{row}'] = detalle.cantidad  # Por ahora solo cantidad, puede expandirse
        row += 1
    
    # Ajustar ancho de columnas
    ws.column_dimensions['A'].width = 40
    ws.column_dimensions['B'].width = 15
    ws.column_dimensions['C'].width = 15
    
    # Respuesta HTTP con el archivo Excel
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    nombre_archivo = f"Pedido_{pedido.nombre.replace(' ', '_')}_{pedido.fecha_creacion.strftime('%Y%m%d')}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
    
    wb.save(response)
    return response


@login_required
def eliminar_pedido_view(request, pedido_id):
    """Vista para eliminar un pedido"""
    if request.user.rol == 'usuario' and request.user.cambio_password_requerido:
        return redirect('cambiar_password')
    if not (request.user.es_administrador() or request.user.is_superuser):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('panel')
    
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    if request.method == 'POST':
        nombre_pedido = pedido.nombre
        pedido.delete()
        messages.success(request, f'Pedido "{nombre_pedido}" eliminado exitosamente.')
        return redirect('ventas_pedidos')
    
    return render(request, 'core/eliminar_pedido.html', {'pedido': pedido})


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
            # Registrar auditoría
            from .utils import registrar_auditoria
            registrar_auditoria(
                usuario=request.user,
                accion='falla_create',
                modulo='operaciones',
                descripcion=f'Falla #{falla.contador_falla} registrada: {falla.maquina}',
                objeto_afectado=f"Falla #{falla.contador_falla}",
                detalles={
                    'contador_falla': falla.contador_falla,
                    'maquina': falla.maquina,
                    'fecha': str(falla.fecha),
                }
            )
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
            # Registrar auditoría
            from .utils import registrar_auditoria
            registrar_auditoria(
                usuario=request.user,
                accion='llamada_create',
                modulo='operaciones',
                descripcion=f'Llamada #{llamada.contador_llamada} registrada: {llamada.motivo}',
                objeto_afectado=f"Llamada #{llamada.contador_llamada}",
                detalles={
                    'contador_llamada': llamada.contador_llamada,
                    'motivo': llamada.motivo,
                    'tecnico_contactado': llamada.tecnico_contactado,
                    'fecha': str(llamada.fecha),
                }
            )
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
            # Registrar auditoría
            from .utils import registrar_auditoria
            registrar_auditoria(
                usuario=request.user,
                accion='falla_edit',
                modulo='operaciones',
                descripcion=f'Falla #{falla.contador_falla} modificada: {falla.maquina}',
                objeto_afectado=f"Falla #{falla.contador_falla}",
                detalles={
                    'contador_falla': falla.contador_falla,
                    'maquina': falla.maquina,
                    'fecha': str(falla.fecha),
                }
            )
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
        maquina = falla.maquina
        fecha = str(falla.fecha)
        falla.delete()
        # Registrar auditoría
        from .utils import registrar_auditoria
        registrar_auditoria(
            usuario=request.user,
            accion='falla_delete',
            modulo='operaciones',
                descripcion=f'Falla #{contador} eliminada: {maquina}',
            objeto_afectado=f"Falla #{contador}",
            detalles={
                'contador_falla': contador,
                'maquina': maquina,
                'fecha': fecha,
            }
        )
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
            # Registrar auditoría
            from .utils import registrar_auditoria
            registrar_auditoria(
                usuario=request.user,
                accion='llamada_edit',
                modulo='operaciones',
                descripcion=f'Llamada #{llamada.contador_llamada} modificada: {llamada.motivo}',
                objeto_afectado=f"Llamada #{llamada.contador_llamada}",
                detalles={
                    'contador_llamada': llamada.contador_llamada,
                    'motivo': llamada.motivo,
                    'tecnico_contactado': llamada.tecnico_contactado,
                    'fecha': str(llamada.fecha),
                }
            )
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
        motivo = llamada.motivo
        tecnico = llamada.tecnico_contactado
        fecha = str(llamada.fecha)
        llamada.delete()
        # Registrar auditoría
        from .utils import registrar_auditoria
        registrar_auditoria(
            usuario=request.user,
            accion='llamada_delete',
            modulo='operaciones',
                descripcion=f'Llamada #{contador} eliminada: {motivo}',
            objeto_afectado=f"Llamada #{contador}",
            detalles={
                'contador_llamada': contador,
                'motivo': motivo,
                'tecnico_contactado': tecnico,
                'fecha': fecha,
            }
        )
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
            usuario_nombre = asistencia.usuario.get_nombre_completo() if asistencia.usuario else 'Usuario Anónimo'
            usuario_nombre_completo = f"{asistencia.usuario.nombre} {asistencia.usuario.apellido}" if asistencia.usuario else 'Usuario Anónimo'
            form.save()
            # Registrar auditoría
            from .utils import registrar_auditoria
            registrar_auditoria(
                usuario=request.user,
                accion='asistencia_edit',
                modulo='asistencia',
                descripcion=f'Asistencia modificada de {usuario_nombre} - Fecha: {asistencia.fecha}, Turno: {asistencia.get_turno_display()}',
                objeto_afectado=usuario_nombre_completo,
                detalles={
                    'usuario': usuario_nombre,
                    'fecha': str(asistencia.fecha),
                    'turno': asistencia.turno,
                }
            )
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
        usuario_nombre = asistencia.usuario.get_nombre_completo() if asistencia.usuario else 'Usuario Anónimo'
        usuario_nombre_completo = f"{asistencia.usuario.nombre} {asistencia.usuario.apellido}" if asistencia.usuario else 'Usuario Anónimo'
        fecha = str(asistencia.fecha)
        turno = asistencia.turno
        turno_display = asistencia.get_turno_display()
        asistencia.delete()
        # Registrar auditoría
        from .utils import registrar_auditoria
        registrar_auditoria(
            usuario=request.user,
            accion='asistencia_delete',
            modulo='asistencia',
                descripcion=f'Asistencia eliminada de {usuario_nombre} - Fecha: {fecha}, Turno: {turno_display}',
            objeto_afectado=usuario_nombre_completo,
            detalles={
                'usuario': usuario_nombre,
                'fecha': fecha,
                'turno': turno,
            }
        )
        messages.success(request, f'Registro de asistencia de {usuario_nombre} eliminado exitosamente.')
        return redirect('asistencia')
    
    return render(request, 'core/eliminar_asistencia.html', {'asistencia': asistencia})


def index_view(request):
    """Vista para la página principal"""
    return render(request, 'core/index.html')


def contactanos_view(request):
    """Vista para la página de contáctanos"""
    # Verificar si el usuario está autenticado
    usuario_autenticado = request.user.is_authenticated
    
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
            'nombre': 'Gerente de Marketing',
            'cargo': 'Gerente de Marketing',
            'email': 'marketing@popupnescafe.cl',
            'telefono': '+56 9 XXXX XXXX',
        },
        {
            'nombre': 'Gerente de Finanzas',
            'cargo': 'Gerente de Finanzas',
            'email': 'finanzas@popupnescafe.cl',
            'telefono': '+56 9 XXXX XXXX',
        },
    ]
    return render(request, 'core/contactanos.html', {
        'contactos': contactos,
        'usuario_autenticado': usuario_autenticado
    })


@login_required
def trabajador_dashboard_view(request):
    """Dashboard principal para usuarios trabajadores"""
    # Solo usuarios trabajadores pueden acceder
    if request.user.rol != 'usuario':
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('panel')
    
    # Si el usuario necesita cambiar su contraseña, redirigir primero
    if request.user.cambio_password_requerido:
        return redirect('cambiar_password')
    
    return render(request, 'core/trabajador_dashboard.html', {
        'usuario': request.user
    })


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
                    # Redirigir al dashboard del trabajador
                    return redirect('trabajador_dashboard')
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
                    # Redirigir al dashboard del trabajador
                    return redirect('trabajador_dashboard')
                
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


@login_required
def cambiar_stock_view(request):
    """Vista para que trabajadores cambien el stock de productos"""
    # Solo usuarios trabajadores pueden cambiar stock
    if request.user.rol != 'usuario':
        messages.error(request, 'Solo los usuarios trabajadores pueden cambiar el stock')
        return redirect('panel')
    
    # Si el usuario necesita cambiar su contraseña, redirigir primero
    if request.user.cambio_password_requerido:
        return redirect('cambiar_password')
    
    # Obtener todos los productos
    productos = Inventario.objects.all().order_by('categoria', 'nombre')
    
    # Organizar productos por categoría
    bodega = productos.filter(categoria='bodega')
    meson = productos.filter(categoria='meson')
    limpieza = productos.filter(categoria='limpieza')
    
    return render(request, 'core/cambiar_stock.html', {
        'bodega': bodega,
        'meson': meson,
        'limpieza': limpieza,
        'usuario': request.user
    })


@login_required
def actualizar_stock_view(request, producto_id):
    """Vista para actualizar el stock de un producto específico (solo trabajadores)"""
    # Solo usuarios trabajadores pueden cambiar stock
    if request.user.rol != 'usuario':
        messages.error(request, 'Solo los usuarios trabajadores pueden cambiar el stock')
        return redirect('panel')
    
    # Si el usuario necesita cambiar su contraseña, redirigir primero
    if request.user.cambio_password_requerido:
        return redirect('cambiar_password')
    
    try:
        producto = Inventario.objects.get(id=producto_id)
    except Inventario.DoesNotExist:
        messages.error(request, 'Producto no encontrado')
        return redirect('cambiar_stock')
    
    form = CambiarStockForm(initial={'cantidad': producto.cantidad})
    
    if request.method == 'POST':
        form = CambiarStockForm(request.POST)
        if form.is_valid():
            cantidad_anterior = producto.cantidad
            nueva_cantidad = form.cleaned_data['cantidad']
            producto.cantidad = nueva_cantidad
            producto.save()
            # Registrar auditoría de cambio de stock
            from .utils import registrar_auditoria
            registrar_auditoria(
                usuario=request.user,
                accion='inventario_stock_change',
                modulo='inventario',
                descripcion=f'Stock de "{producto.nombre}" cambió de {cantidad_anterior} a {nueva_cantidad} unidades',
                objeto_afectado=producto.nombre,
                detalles={
                    'cantidad_anterior': cantidad_anterior,
                    'cantidad_nueva': nueva_cantidad,
                    'diferencia': nueva_cantidad - cantidad_anterior,
                    'categoria': producto.categoria,
                }
            )
            messages.success(request, f'Stock de "{producto.nombre}" actualizado a {nueva_cantidad} unidades')
            return redirect('cambiar_stock')
    
    return render(request, 'core/actualizar_stock.html', {
        'producto': producto,
        'form': form,
        'usuario': request.user
    })


@login_required
def auditoria_view(request):
    """Vista para ver los registros de auditoría"""
    # Solo administradores pueden ver la auditoría
    if not (request.user.es_administrador() or request.user.is_superuser):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('panel')
    
    # Obtener todos los registros de auditoría
    registros = Auditoria.objects.all().select_related('usuario')
    
    # Filtros
    modulo_filter = request.GET.get('modulo', '')
    accion_filter = request.GET.get('accion', '')
    usuario_filter = request.GET.get('usuario', '')
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')
    search_query = request.GET.get('search', '')
    
    # Aplicar filtros
    if modulo_filter:
        registros = registros.filter(modulo=modulo_filter)
    if accion_filter:
        registros = registros.filter(accion=accion_filter)
    if usuario_filter:
        registros = registros.filter(usuario_id=usuario_filter)
    if fecha_desde:
        registros = registros.filter(fecha_hora__date__gte=fecha_desde)
    if fecha_hasta:
        registros = registros.filter(fecha_hora__date__lte=fecha_hasta)
    if search_query:
        registros = registros.filter(
            Q(descripcion__icontains=search_query) |
            Q(objeto_afectado__icontains=search_query) |
            Q(usuario__username__icontains=search_query) |
            Q(usuario__nombre__icontains=search_query) |
            Q(usuario__apellido__icontains=search_query)
        )
    
    # Ordenar por fecha más reciente
    registros = registros.order_by('-fecha_hora')
    
    # Paginación (opcional, por ahora mostramos todos)
    # registros = registros[:100]  # Limitar a los últimos 100 registros
    
    # Obtener opciones para los filtros
    usuarios = Usuario.objects.all().order_by('username')
    
    context = {
        'registros': registros,
        'usuarios': usuarios,
        'modulos': Auditoria.MODULO_CHOICES,
        'acciones': Auditoria.ACCION_CHOICES,
        'modulo_filter': modulo_filter,
        'accion_filter': accion_filter,
        'usuario_filter': usuario_filter,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'search_query': search_query,
    }
    
    return render(request, 'core/auditoria.html', context)

