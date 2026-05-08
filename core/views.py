from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from .models import Categoria, Transaccion, ReglaAutomatica
from .motor_reglas import MotorCategorizacion

@login_required(login_url='/accounts/login/')
def dashboard(request):
    """
    Vista principal del panel de control.
    Calcula ingresos, gastos y balance total del usuario autenticado.
    También agrupa los gastos por categoría para alimentar el gráfico de torta.
    """
    mis_transacciones = Transaccion.objects.filter(usuario=request.user)
    ingresos = mis_transacciones.filter(tipo='ingreso').aggregate(Sum('monto'))['monto__sum'] or 0
    gastos   = mis_transacciones.filter(tipo='gasto').aggregate(Sum('monto'))['monto__sum'] or 0
    balance  = ingresos - gastos

    # Agrupamos gastos por categoría para el gráfico de torta (Chart.js en el template)
    gastos_por_categoria = mis_transacciones.filter(tipo='gasto').values(
        'categoria__nombre'
    ).annotate(total=Sum('monto')).order_by('-total')

    contexto = {
        'transacciones': mis_transacciones,
        'balance': balance,
        'ingresos': ingresos,
        'gastos': gastos,
        'grafico_categorias': list(gastos_por_categoria),
    }
    return render(request, 'dashboard.html', contexto)

@login_required(login_url='/accounts/login/')
def guardar_gasto(request):
    """
    Crea una nueva transacción (ingreso o gasto) para el usuario autenticado.

    Flujo:
      1. Captura los datos del formulario (monto, tipo, descripción, texto crudo).
      2. Carga las reglas automáticas del usuario y construye el diccionario del motor.
      3. El MotorCategorizacion analiza el texto y devuelve el nombre de la categoría.
      4. Busca o crea esa categoría en la BD y la asocia a la nueva transacción.
      5. Redirige al dashboard.
    """
    if request.method == 'POST':
        raw  = request.POST.get('raw_text', '')
        desc = request.POST.get('descripcion', '')

        # Construir diccionario {palabra_clave: nombre_categoria} para el motor
        reglas_db  = ReglaAutomatica.objects.filter(usuario=request.user)
        diccionario = {r.palabra_clave: r.categoria_asignada.nombre for r in reglas_db}

        # El motor analiza el texto crudo primero; si no hay, analiza la descripción
        motor           = MotorCategorizacion(diccionario)
        texto_analizar  = raw if raw else desc
        nombre_categoria = motor.analizar(texto_analizar)

        # Busca la categoría en BD o la crea si no existe
        categoria_obj, _ = Categoria.objects.get_or_create(
            nombre=nombre_categoria,
            usuario=request.user
        )

        Transaccion.objects.create(
            usuario=request.user,
            monto=request.POST.get('monto'),
            tipo=request.POST.get('tipo'),
            descripcion=desc,
            categoria=categoria_obj,
            raw_text=raw
        )
        return redirect('dashboard')

    # GET: muestra el formulario vacío
    return render(request, 'Transacciones/transacciones_form.html')

def index(request):
    # Si el usuario ya inició sesión y entra a la raíz, puede redirigirlo al dashboard por comodidad
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    return render(request, 'index.html')


@login_required(login_url='/accounts/login/')
def reglas_list(request):
    """Lista todas las reglas automáticas del usuario y permite crear nuevas."""
    categorias = Categoria.objects.filter(usuario=request.user)
    reglas = ReglaAutomatica.objects.filter(usuario=request.user).select_related('categoria_asignada')

    if request.method == 'POST':
        palabra = request.POST.get('palabra_clave', '').strip().lower()
        cat_id = request.POST.get('categoria_id')
        nueva_cat_nombre = request.POST.get('nueva_categoria', '').strip()

        # Si escribió una categoría nueva, la creamos; si no, usamos la seleccionada
        if nueva_cat_nombre:
            categoria_obj, _ = Categoria.objects.get_or_create(
                nombre=nueva_cat_nombre, usuario=request.user
            )
        elif cat_id:
            categoria_obj = get_object_or_404(Categoria, pk=cat_id, usuario=request.user)
        else:
            messages.error(request, 'Debes seleccionar o crear una categoría.')
            return redirect('reglas_list')

        if not palabra:
            messages.error(request, 'La palabra clave no puede estar vacía.')
            return redirect('reglas_list')

        # Evitar duplicados: si ya existe esa palabra clave para este usuario, actualizar
        regla, creada = ReglaAutomatica.objects.update_or_create(
            usuario=request.user,
            palabra_clave=palabra,
            defaults={'categoria_asignada': categoria_obj}
        )
        if creada:
            messages.success(request, f'Regla "{palabra}" creada exitosamente.')
        else:
            messages.warning(request, f'Regla "{palabra}" actualizada a la categoría "{categoria_obj.nombre}".')

        return redirect('reglas_list')

    contexto = {
        'reglas': reglas,
        'categorias': categorias,
    }
    return render(request, 'reglas/reglas_list.html', contexto)


@login_required(login_url='/accounts/login/')
def eliminar_regla(request, regla_id):
    """Elimina una regla automática por su ID (sólo acepta POST para seguridad)."""
    regla = get_object_or_404(ReglaAutomatica, pk=regla_id, usuario=request.user)
    if request.method == 'POST':
        nombre = regla.palabra_clave
        regla.delete()
        messages.success(request, f'Regla "{nombre}" eliminada.')
    return redirect('reglas_list')