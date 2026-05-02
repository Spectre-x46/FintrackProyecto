from django.contrib import admin
from django.urls import path
from core.views import dashboard, guardar_gasto, index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('guardar_gasto/', guardar_gasto, name='guardar_gasto'),
]