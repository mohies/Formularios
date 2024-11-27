from django.shortcuts import render,redirect
from .models import *
from django.db.models import Prefetch,Count,Q
from .forms import *
from django.contrib import messages

def index(request):
    return render(request, 'index.html')



def crear_torneo(request):
    
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
        
    formulario = TorneoForm(datosFormulario)
    if (request.method == "POST"):
        if formulario.is_valid():
            try:
                # Guarda el libro en la base de datos
                formulario.save()
                return redirect("index")
            except Exception as error:
                print(error)
    
    return render(request, 'torneo/formulario/crear_torneo.html', {'formulario': formulario}) 


def crear_equipo(request):
    datosFormulario = None  # Esto es para capturar los datos del formulario si se envían por POST

    # Si la solicitud es POST, significa que se está enviando el formulario
    if request.method == "POST":
        datosFormulario = request.POST
        
    formulario = EquipoForm(datosFormulario)  # Creamos una instancia del formulario con los datos de la solicitud
    if request.method == "POST" and formulario.is_valid():  # Si el formulario es válido
        try:
            formulario.save()  # Guarda el equipo en la base de datos
            return redirect("index")  # Redirige al índice o la página que desees
        except Exception as error:
            print(error)  # Imprime el error si ocurre alguno

    return render(request, 'torneo/formulario/crear_equipo.html', {'formulario': formulario})  # Renderiza el formulario








#Distintos errores de las paginas web
def mi_error_404(request, exception=None):
    return render(request, 'torneo/errores/404.html', None,None,404)
def mi_error_400(request, exception=None):
    return render(request, 'torneo/errores/400.html', None,None,400)
def mi_error_403(request, exception=None):
    return render(request, 'torneo/errores/403.html', None,None,403)
def mi_error_500(request, exception=None):
    return render(request, 'torneo/errores/403.html', None,None,500)

