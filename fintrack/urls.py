from django.contrib import admin
from django.urls import path
from core.views import dashboard, guardar_gasto

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('guardar_gasto/', guardar_gasto, name='guardar_gasto'),
]