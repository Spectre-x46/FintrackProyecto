from django.contrib import admin
from django.urls import include, path
from core.views import dashboard, guardar_gasto, index

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('guardar_gasto/', guardar_gasto, name='guardar_gasto'),
]
