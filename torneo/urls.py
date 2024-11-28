from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lista',views.lista_torneo,name='lista_torneo'),
    path('crear-torneo/', views.crear_torneo, name='crear_torneo'),
    path('crear-equipo/', views.crear_equipo, name='crear_equipo'),  # Nueva ruta para crear equipo
    path('buscar_torneo/', views.torneo_buscar_avanzado, name='buscar_torneo'),
]
