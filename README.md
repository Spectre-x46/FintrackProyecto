# FinTrack

FinTrack es un proyecto Django en desarrollo para la gestión simple de finanzas personales con autenticación de usuarios y motor de categorización automática de transacciones. Actualmente incluye una página de dashboard básica y modelos para usuarios, categorías, transacciones y reglas automáticas de clasificación.

**Autores**: Gabriela Alvarado, Felipe Droguett, Rodrigo Villaroel.

## Estado actual

- Proyecto Django 6.0 con autenticación de usuarios implementada.
- Aplicación principal: `core`.
- Dashboard disponible en `/dashboard/` (requiere autenticación).
- Página de inicio en la ruta raíz (`/`) con opción de login.
- Plantilla principal: `templates/base.html` con Bootstrap 5, Font Awesome y SweetAlert.
- Base de datos conectada a PostgreSQL mediante variables de entorno (últimas transacciones guardadas en BD).
- Sistema de autenticación configurado con `django.contrib.auth` y `django.contrib.auth.urls`.

## Componentes principales

- `manage.py` - utilidad de Django para ejecutar comandos.
- `fintrack/settings.py` - configuración del proyecto (incluye PostgreSQL, autenticación, middlewares de seguridad).
- `fintrack/urls.py` - enrutamiento principal del proyecto (admin, core routes y autenticación).
- `core/urls.py` - rutas de la aplicación core (index, dashboard, guardar_gasto).
- `core/models.py` - definiciones de datos para:
  - `User` - modelo de usuario estándar de Django
  - `Categoria` - categorías de transacciones (vinculadas al usuario)
  - `ReglaAutomatica` - reglas para asignar categorías automáticamente según palabra clave
  - `Transaccion` - registro de ingresos y gastos con categoría, descripción y texto raw
- `core/motor_reglas.py` - motor de categorización automática que analiza texto y asigna categorías según reglas del usuario.
- `core/views.py` - vistas principales:
  - `index()` - página de inicio que redirige a dashboard si está autenticado
  - `dashboard()` - panel de control que muestra ingresos, gastos, balance y transacciones (requiere login)
  - `guardar_gasto()` - formulario para crear nuevas transacciones con categorización automática
- `templates/base.html` - plantilla base del proyecto con navegación y pie de página.
- `templates/dashboard.html` - plantilla del dashboard con tarjetas de resumen financiero.
- `templates/registration/login.html` - formulario de autenticación con validación de errores.
- `templates/index.html` - página de inicio con acceso a login.

## Tecnologías

- **Backend**: Python 3.x, Django 6.0
- **Base de datos**: PostgreSQL
- **Frontend**: HTML5, Bootstrap 5, CSS personalizado
- **Librerías**: Font Awesome (iconos), SweetAlert (alertas), django-decouple (variables de entorno)
- **Autenticación**: Django Auth (contrib.auth)

## Características principales

### Motor de Categorización Automática
- El `MotorCategorizacion` analiza textos ingresados por el usuario y los clasifica automáticamente.
- Utiliza palabras clave definidas por el usuario en sus reglas personalizadas.
- Si coincide una palabra clave en el texto, asigna la categoría asociada automáticamente.
- Si no encuentra coincidencia, clasifica como "Sin Categoría".

### Sistema de Autenticación
- Implementado con `django.contrib.auth` y decorador `@login_required`.
- Usuarios redirigidos a `/accounts/login/` si no están autenticados.
- Después del login, se redirige al dashboard.
- Página de inicio verifica si el usuario está autenticado y lo redirige apropiadamente.

### Dashboard
- Muestra resumen de ingresos, gastos y balance general del usuario.
- Calcula métricas directamente desde la base de datos (suma de montos por tipo).
- Permite navegar a formularios de transacciones.

### Gestión de Transacciones
- Formulario para crear nuevas transacciones (`Transacciones/transacciones_form.html`).
- Captura tipo (ingreso/gasto), monto, descripción y texto raw.
- Categorización automática mediante el motor de reglas.
- Almacenamiento en PostgreSQL con relación al usuario autenticado.

## Requisitos

Asegúrate de tener instalado:

- Python 3.8 o superior
- PostgreSQL 10 o superior
- pip (gestor de paquetes de Python)
- Un entorno virtual (recomendado)

## Configuración local

1. Clona el repositorio desde GitHub.

2. Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En macOS/Linux:
   source venv/bin/activate
   ```

3. Instala las dependencias:
   ```bash
   pip install django python-decouple psycopg2-binary
   ```

4. Crea un archivo `.env` en la raíz del proyecto con los siguientes valores:
   ```env
   DB_NAME=nombre_de_tu_bd
   DB_USER=usuario_bd
   DB_PASSWORD=tu_contraseña
   DB_HOST=localhost
   DB_PORT=5432
   ```
   
   **Nota**: Asegúrate de que PostgreSQL esté corriendo y la base de datos exista.

5. Aplica migraciones para crear las tablas:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. (Opcional) Crea un superusuario para acceder al panel de administración:
   ```bash
   python manage.py createsuperuser
   ```
   Se accede en `/admin/` con credenciales de superusuario.

7. Ejecuta el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

8. Abre tu navegador en `http://127.0.0.1:8000/`.

## Flujo de uso

1. **Página de Inicio**: Accede a `http://127.0.0.1:8000/`.
2. **Login**: Ingresa credenciales de usuario registrado (o crea uno vía admin).
3. **Dashboard**: Visualiza resumen de ingresos, gastos y balance.
4. **Crear Transacción**: Completa el formulario en `/guardar_gasto/` con detalles de la transacción.
5. **Categorización Automática**: El motor analiza el texto ingresado y asigna categoría automáticamente.
6. **Registro en BD**: La transacción se guarda en PostgreSQL asociada a tu usuario.

## Próximos pasos sugeridos

- Mejorar el dashboard: mostrar datos reales de ingresos, gastos y balance dinámicamente.
- Implementar edición y eliminación de transacciones.
- Crear interfaz para gestionar categorías personalizadas y reglas automáticas.
- Agregar gráficos de análisis de gastos (pie charts, line charts).
- Implementar reportes por período (mensual, anual).
- Añadir exportación de datos (CSV, PDF).
- Validar montos en transacciones (usar decimales en lugar de enteros).
- Implementar paginación en listado de transacciones.
- Mejorar la experiencia de usuario con más feedback visual (SweetAlert confirmaciones).
- Agregar pruebas unitarias e integración.
- Desplegar en servidor de producción y configurar variables de seguridad.

## Historial de cambios recientes

- **Última actualización (May 2, 2026)**: Conexión de transacciones a BD implementada.
- **Commits previos**: Configuración de autenticación con `@login_required`, reorganización de URLs en jerarquías Core y FinTrack, resolución de conflictos de fusión, implementación de formularios y vistas de transacciones.
- **Migraciones**: Tabla de transacciones conectada a usuarios, categorías y reglas automáticas.

## Notas de desarrollo

- El dashboard actualmente muestra estructura de tarjetas pero necesita integración con contexto dinámico de datos.
- El campo `monto` en la tabla `Transaccion` está como `IntegerField` (considera usar `DecimalField` para cantidades monetarias).
- El motor de reglas es sensible a mayúsculas/minúsculas (convierte todo a minúsculas antes de comparar).
- La autenticación está en funcionamiento; todas las vistas críticas están protegidas con `@login_required`.
- PostgreSQL debe estar corriendo y accesible para que la aplicación funcione correctamente.
