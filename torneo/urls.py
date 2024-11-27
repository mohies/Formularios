from django.urls import path
from . import views

urlpatterns = [
    path('', views.crear_torneo, name='crear_torneo'),
    path('crear-equipo/', views.crear_equipo, name='crear_equipo'),  # Nueva ruta para crear equipo
]
