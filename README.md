# FinTrack

FinTrack es una aplicación web Django para la **gestión inteligente de finanzas personales**. Permite registrar ingresos y gastos, visualizarlos en un dashboard con gráficos en tiempo real, y automatizar la categorización de transacciones mediante un motor de reglas personalizadas.

**Autores**: Gabriela Alvarado, Felipe Droguett, Rodrigo Villaroel.

---

## Estado actual del proyecto

| Módulo | Estado |
|---|---|
| Autenticación (Login / Logout) | ✅ Implementado |
| Dashboard con métricas dinámicas | ✅ Implementado |
| Gráfico de gastos por categoría (Chart.js) | ✅ Implementado |
| Formulario de nueva transacción | ✅ Implementado |
| Motor de categorización automática (Regex) | ✅ Implementado |
| Gestión de Reglas Automáticas (CRUD) | ✅ Implementado |
| Modelos con DecimalField y __str__ | ✅ Implementado |
| Conexión a banco vía API (Fintoc/Belvo) | 🔜 Próximo paso |
| Filtros por período (mes/año) | 🔜 Próximo paso |
| Exportar reportes (CSV/PDF) | 🔜 Próximo paso |

---

## Arquitectura del Proyecto

```
FintrackProyecto-main/
├── fintrack/               # Configuración global del proyecto Django
│   ├── settings.py         # BD, autenticación, apps instaladas
│   └── urls.py             # Enrutador raíz: /admin, /accounts, /core
│
├── core/                   # Aplicación principal
│   ├── models.py           # Modelos: Categoria, ReglaAutomatica, Transaccion
│   ├── views.py            # Vistas: dashboard, guardar_gasto, reglas_list, eliminar_regla
│   ├── urls.py             # Rutas: /, /dashboard/, /guardar_gasto/, /reglas/
│   └── motor_reglas.py     # Clase MotorCategorizacion (clasificación automática)
│
├── templates/
│   ├── base.html           # Plantilla base con navbar y mensajes flash globales
│   ├── index.html          # Página de inicio (redirige al dashboard si hay sesión)
│   ├── dashboard.html      # Panel principal con métricas y gráfico de torta
│   ├── registration/
│   │   └── login.html      # Formulario de inicio de sesión
│   ├── Transacciones/
│   │   └── transacciones_form.html  # Formulario para registrar ingreso/gasto
│   └── reglas/
│       └── reglas_list.html         # Gestión de reglas automáticas del motor
│
└── static/                 # Archivos CSS, JS e imágenes propios del proyecto
```

---

## Cómo funciona el Motor de Categorización

1. El usuario define **Reglas Automáticas** en `/reglas/`: pares `{palabra_clave: categoría}`.
   - Ejemplo: `rappi` → `Delivery`, `uber` → `Transporte`.
2. Al registrar una transacción, el texto es analizado por `MotorCategorizacion`.
3. El motor busca cada palabra clave usando **Expresiones Regulares** (palabras completas, no subcadenas).
4. Si hay coincidencia, asigna la categoría automáticamente. Si no, queda como `Sin Categoría`.

---

## Tecnologías

| Categoría | Tecnología |
|---|---|
| Backend | Python 3.x, Django 6.0 |
| Base de Datos | PostgreSQL |
| Frontend | Bootstrap 5, Chart.js, Font Awesome, SweetAlert2 |
| Autenticación | Django Auth (`django.contrib.auth`) |
| Variables de Entorno | `python-decouple` |

---

## Requisitos

- Python 3.8+
- PostgreSQL 10+
- pip

---

## Configuración local

```bash
# 1. Clonar el repositorio
git clone <url-del-repo>

# 2. Crear y activar entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Instalar dependencias
pip install django python-decouple psycopg2-binary bcrypt

# 4. Crear el archivo .env en la raíz
# DB_NAME=nombre_bd
# DB_USER=usuario_bd
# DB_PASSWORD=contraseña
# DB_HOST=localhost
# DB_PORT=5432

# 5. Aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# 6. (Opcional) Crear superusuario para el admin
python manage.py createsuperuser

# 7. Iniciar servidor
python manage.py runserver
```

Accede en: `http://127.0.0.1:8000`

---

## Flujo de uso

1. **Login** → Ingresa con tu usuario en `/accounts/login/`.
2. **Dashboard** → Visualiza tus ingresos, gastos, balance y el gráfico de torta por categoría.
3. **Nueva Transacción** → En `/guardar_gasto/`, registra un ingreso o gasto. Puedes pegar el texto crudo del banco y el motor lo categoriza solo.
4. **Motor de Reglas** → En `/reglas/`, configura tus palabras clave para que la app aprenda tus patrones de gasto.

---

## Historial de cambios

| Fecha | Cambios |
|---|---|
| Mayo 8, 2026 | Rediseño completo del UI (Bootstrap 5 + Chart.js). CRUD de reglas automáticas. Fix bug redirección post-login. Fix bug diccionario de categorías. Motor de reglas mejorado con Regex. Docstrings y comentarios de negocio en todo el código. |
| Mayo 2, 2026 | Conexión de transacciones a BD implementada. |
| Commits previos | Autenticación con `@login_required`, reorganización de URLs, implementación de formularios y vistas de transacciones. |

---

## Próximos pasos

1. **Filtros por período**: Ver dashboard filtrado por mes o año.
2. **Multicuenta**: Separar gastos por cuenta bancaria (Corriente, Crédito, Efectivo).
3. **Integración Open Banking**: Conectar con [Fintoc](https://fintoc.com) o [Belvo](https://belvo.com) para importar transacciones automáticamente desde el banco.
4. **Pruebas unitarias**: Cubrir el `MotorCategorizacion` y las vistas con tests de Django.

---

## Notas de desarrollo

- El campo `monto` usa `DecimalField` para precisión financiera real.
- El motor de reglas convierte todo a minúsculas antes de comparar (insensible a mayúsculas).
- Los webhooks futuros de bancos deberán validarse con firma criptográfica (`X-Fintoc-Signature`).
- `DEBUG = True` solo para desarrollo local. Nunca desplegar en producción con ese valor.
