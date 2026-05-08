from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Sum
from .models import Categoria, Transaccion, ReglaAutomatica
from .motor_reglas import MotorCategorizacion

@login_required(login_url='/accounts/login/')
def dashboard(request):
    # Filtra transacciones y calcula métricas en la BD[cite: 1]
    mis_gastos = Transaccion.objects.filter(usuario=request.user)
    ingresos = mis_gastos.filter(tipo='ingreso').aggregate(Sum('monto'))['monto__sum'] or 0
    gastos = mis_gastos.filter(tipo='gasto').aggregate(Sum('monto'))['monto__sum'] or 0
    balance = ingresos - gastos
    
    # Agrupamos los datos para poder dibujar gráficos de Torta/Barras en el frontend
    gastos_por_categoria = mis_gastos.filter(tipo='gasto').values(
        'categoria__nombre'
    ).annotate(total=Sum('monto')).order_by('-total')

    contexto = {
        'transacciones': mis_gastos,
        'balance': balance,
        'ingresos': ingresos,
        'gastos': gastos,
        'grafico_categorias': list(gastos_por_categoria)
    }
    return render(request, 'dashboard.html', contexto)

@login_required(login_url='/accounts/login/')
def guardar_gasto(request):
    if request.method == 'POST':
        # Captura de datos
        raw = request.POST.get('raw_text', '')
        desc = request.POST.get('descripcion')
        
        # Obtener reglas del usuario y armar el diccionario[cite: 1]
        reglas_db = ReglaAutomatica.objects.filter(usuario=request.user)
        # BUG FIX: Usar el nombre de la categoría, no la instancia de la BD
        diccionario = {r.palabra_clave: r.categoria_asignada.nombre for r in reglas_db}
        
        # Inicializar el motor y analizar el texto[cite: 1]
        motor = MotorCategorizacion(diccionario)
        texto_analizar = raw if raw else desc
        nombre_categoria = motor.analizar(texto_analizar)

        categoria_obj, _ = Categoria.objects.get_or_create(
            nombre=nombre_categoria,
            usuario=request.user
        )

        # Guardar la transacción[cite: 1]
        Transaccion.objects.create(
            usuario=request.user, 
            monto=request.POST.get('monto'),
            tipo=request.POST.get('tipo'),
            descripcion=desc,
            categoria=categoria_obj, 
            raw_text=raw
        )
        return redirect('dashboard')
    
    # Manejo del GET: Muestra el formulario vacío
    return render(request, 'Transacciones/transacciones_form.html')

def index(request):
    # Si el usuario ya inició sesión y entra a la raíz, puede redirigirlo al dashboard por comodidad
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    return render(request, 'index.html')