from django.contrib import admin
from django.urls import include, path
from core.views import dashboard, guardar_gasto, index, reglas_list, eliminar_regla

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('guardar_gasto/', guardar_gasto, name='guardar_gasto'),
    path('reglas/', reglas_list, name='reglas_list'),
    path('reglas/eliminar/<int:regla_id>/', eliminar_regla, name='eliminar_regla'),
]
