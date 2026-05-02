from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)

class ReglaAutomatica(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    palabra_clave = models.CharField(max_length=50)
    categoria_asignada = models.ForeignKey(Categoria, on_delete=models.CASCADE)

class Transaccion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    monto = models.IntegerField()
    tipo = models.CharField(max_length=10, choices=[('ingreso', 'Ingreso'), ('gasto', 'Gasto')])
    descripcion = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    raw_text = models.TextField(blank=True, null=True)