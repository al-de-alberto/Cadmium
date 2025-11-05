# CADMIUM - Sistema de Gestión

Sistema de gestión desarrollado con Django + PostgreSQL para PopUp Nescafe.

## Características

- **Página Principal (Index)**: Página de inicio con carrusel de imágenes, noticias y eventos
- **Sistema de autenticación**: Login seguro para acceder al sistema
- **Panel de administrador** con tres módulos principales:
  - **Usuarios**: Gestión de usuarios del sistema
  - **Inventario**: Control de inventario
  - **Asistencia**: Registro de asistencias
- **Página de Contacto**: Información de contacto de la gerencia

## Instalación

### 1. Crear entorno virtual (recomendado)

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar PostgreSQL

1. Crear una base de datos llamada `cadmium_db`
2. Actualizar las credenciales en `cadmium/settings.py` si es necesario:
   - USER: 'postgres'
   - PASSWORD: 'postgres'
   - HOST: 'localhost'
   - PORT: '5432'

### 4. Ejecutar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear usuario administrador

```bash
python manage.py create_gerencia
```

O usar el comando estándar de Django:
```bash
python manage.py createsuperuser
```

**Credenciales del administrador:**
- Usuario: `Gerencia`
- Contraseña: `Ger_2O25`

### 6. Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

El sistema estará disponible en: http://127.0.0.1:8000/

## Estructura del Proyecto

```
cadmium/
├── cadmium/          # Configuración del proyecto
├── core/             # App principal
│   ├── models.py     # Modelos: Usuario, Inventario, Asistencia
│   ├── views.py      # Vistas del sistema
│   ├── urls.py       # URLs de la app
│   └── admin.py      # Configuración del admin de Django
├── templates/        # Templates HTML
├── static/          # Archivos estáticos (CSS, JS)
└── manage.py        # Script de gestión de Django
```

## Modelos

### Usuario
- Extiende de AbstractUser
- Campos: username, email, rol, activo, fecha_creacion

### Inventario
- Campos: nombre, descripcion, cantidad, precio_unitario, categoria

### Asistencia
- Campos: usuario, fecha, hora_entrada, hora_salida, estado, observaciones

## Notas

- El sistema utiliza un modelo de Usuario personalizado
- Solo los usuarios con rol de administrador pueden acceder al panel
- El panel incluye estadísticas generales y navegación entre secciones



