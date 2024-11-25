from django.urls import path, re_path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('crear-torneo/', views.crear_torneo, name='crear_torneo'),

]