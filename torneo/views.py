from django.shortcuts import render
from .models import *
from django.db.models import Prefetch,Count,Q
from .forms import TorneoForm
# Create your views here.
def index(request):
    return render(request, 'index.html')

def crear_torneo(request):
    if request.method == "POST":
        # Procesar datos enviados
        form = TorneoForm(request.POST)
        if form.is_valid():
            # Aquí puedes manejar los datos del formulario
            # Por ejemplo, crear una instancia del modelo Torneo
            # torneo = Torneo.objects.create(**form.cleaned_data)
            # torneo.save()
            return render(request, 'exito.html')  # Redirigir a una página de éxito
    else:
        # Mostrar el formulario vacío
        form = TorneoForm()
    
    return render(request, 'torneo/formulario/crear_torneo.html', {'formulario': form})


#Distintos errores de las paginas web
def mi_error_404(request, exception=None):
    return render(request, 'torneo/errores/404.html', None,None,404)
def mi_error_400(request, exception=None):
    return render(request, 'torneo/errores/400.html', None,None,400)
def mi_error_403(request, exception=None):
    return render(request, 'torneo/errores/403.html', None,None,403)
def mi_error_500(request, exception=None):
    return render(request, 'torneo/errores/403.html', None,None,500)

