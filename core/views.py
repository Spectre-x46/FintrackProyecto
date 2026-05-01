from django.shortcuts import render, redirect
from .models import Transaccion

def dashboard(request):
    return render(request, 'Login/login.html')

def guardar_gasto(request):
    if request.method == 'POST':
        Transaccion.objects.create(
            usuario=request.user,
            monto=request.POST.get('monto'),
            tipo=request.POST.get('tipo'),
            descripcion=request.POST.get('descripcion'),
            categoria_id=request.POST.get('categoria'),
            raw_text=request.POST.get('raw_text', '')
        )
        return redirect('dashboard')
    return render(request, 'Transacciones/transacciones_form.html')
