from django.db import models
from django.contrib.auth.models import User

# Etiqueta personalizada por usuario (ej: "Supermercado", "Transporte", "Entretenimiento")
class Categoria(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre  = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

# Regla del motor: si el texto de una transacción contiene 'palabra_clave', se asigna 'categoria_asignada'
class ReglaAutomatica(models.Model):
    usuario            = models.ForeignKey(User, on_delete=models.CASCADE)
    palabra_clave      = models.CharField(max_length=50)
    categoria_asignada = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.palabra_clave} -> {self.categoria_asignada.nombre}"

# Registro de un movimiento de dinero: puede ser un ingreso o un gasto
class Transaccion(models.Model):
    usuario     = models.ForeignKey(User, on_delete=models.CASCADE)
    monto       = models.DecimalField(max_digits=12, decimal_places=2)  # Siempre positivo; el tipo define si es ingreso o gasto
    tipo        = models.CharField(max_length=10, choices=[('ingreso', 'Ingreso'), ('gasto', 'Gasto')])
    descripcion = models.CharField(max_length=200)
    categoria   = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    raw_text    = models.TextField(blank=True, null=True)  # Texto original pegado desde el banco/SMS

    def __str__(self):
        return f"{self.tipo.capitalize()} - ${self.monto} ({self.descripcion})"