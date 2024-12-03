from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lista',views.lista_torneo,name='lista_torneo'),
    path('crear-torneo/', views.crear_torneo, name='crear_torneo'),
    path('crear-equipo/', views.crear_equipo, name='crear_equipo'),  # Nueva ruta para crear equipo
    path('buscar_torneo/', views.torneo_buscar_avanzado, name='buscar_torneo'),
    path('torneo/editar/<int:torneo_id>/', views.torneo_editar, name='torneo_editar'),
    path('torneo/eliminar/<int:torneo_id>/', views.torneo_eliminar, name='torneo_eliminar'),
    path('buscar_equipo/', views.equipo_buscar_avanzado, name='buscar_equipo'),
    path('listaequipo',views.lista_equipos,name='lista_equipos'),
    path('equipo/editar/<int:equipo_id>/', views.equipo_editar, name='equipo_editar'),
    path('equipo/eliminar/<int:equipo_id>/', views.equipo_eliminar, name='equipo_eliminar'),
    path('crear-participante/', views.crear_participante, name='crear_participante'),
    

]
