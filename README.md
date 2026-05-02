# FinTrack

FinTrack es un proyecto Django en desarrollo para la gestión simple de finanzas personales. Actualmente incluye una página de dashboard básica y modelos para usuarios, categorías, transacciones y reglas automáticas de clasificación.

## Estado actual

- Proyecto Django 6.0.
- Aplicación principal: `core`.
- Dashboard básico disponible en la ruta raíz (`/`).
- Plantilla principal: `templates/base.html`.
- Base de datos configurada para PostgreSQL mediante variables de entorno.

## Componentes principales

- `manage.py` - utilidad de Django para ejecutar comandos.
- `fintrack/settings.py` - configuración del proyecto.
- `fintrack/urls.py` - enrutamiento de URL del proyecto.
- `core/models.py` - definiciones de datos para:
  - `User` (usuario personalizado simple)
  - `Categoria` (categorías de transacciones)
  - `ReglaAutomatica` (reglas para asignar categorías según palabra clave)
  - `Transaccion` (registro de ingresos y gastos)
- `core/views.py` - vista del dashboard.
- `templates/base.html` - plantilla base del dashboard.

## Tecnologías

- Python
- Django
- PostgreSQL
- Bootstrap 5
- Font Awesome
- SweetAlert

## Requisitos

Asegúrate de tener instalado:

- Python 3.x
- PostgreSQL
- Un entorno virtual opcional

## Configuración local

1. Clona el repositorio.
2. Crea y activa un entorno virtual.
3. Instala Django y las dependencias necesarias (por ejemplo `python-decouple`).
4. Crea un archivo `.env` con los siguientes valores:

```env
DB_NAME=nombre_de_tu_bd
DB_USER=usuario_bd
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432
```

5. Aplica migraciones:

```bash
python manage.py makemigrations
python manage.py migrate
```

6. Crea un superusuario si deseas acceder al admin:

```bash
python manage.py createsuperuser
```

7. Ejecuta el servidor:

```bash
python manage.py runserver
```

8. Abre el navegador en `http://127.0.0.1:8000/`.

## Próximos pasos sugeridos

- Añadir formularios y vistas para crear y editar transacciones.
- Implementar autenticación de usuarios con `django.contrib.auth`.
- Completar el dashboard con datos reales de ingresos, gastos y balance.
- Añadir pruebas automatizadas.
- Mejorar la interfaz con más componentes Bootstrap.

## Notas

- Actualmente la vista del dashboard es estática y muestra valores de ejemplo (`$0`).
- La configuración de PostgreSQL depende de variables de entorno en `.env`.
