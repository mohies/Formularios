from django.shortcuts import render
from .models import *
from django.db.models import Prefetch,Count,Q
from .forms import TorneoForm
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def crear_torneo(request):
    formulario=TorneoForm()
    return render(request, 'torneo/formulario/crear_torneo.html', {'formulario': formulario})


#Distintos errores de las paginas web
def mi_error_404(request, exception=None):
    return render(request, 'torneo/errores/404.html', None,None,404)
def mi_error_400(request, exception=None):
    return render(request, 'torneo/errores/400.html', None,None,400)
def mi_error_403(request, exception=None):
    return render(request, 'torneo/errores/403.html', None,None,403)
def mi_error_500(request, exception=None):
    return render(request, 'torneo/errores/403.html', None,None,500)

