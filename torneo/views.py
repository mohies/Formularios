from django.shortcuts import render,redirect
from .models import *
from django.db.models import Prefetch,Count,Q
from .forms import *
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def lista_torneo(request):
    torneos = Torneo.objects.prefetch_related('participantes__usuario'   ).all()
    return render(request, 'torneo/lista_torneo.html', {'torneos': torneos})



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


"""
def buscar_torneo(request):
    formulario = BusquedaTorneoForm(request.GET)

    if formulario.is_valid():
        texto = formulario.cleaned_data.get('textoBusqueda')
        torneos = Torneo.objects.all()
        torneos = torneos.filter(
            Q(nombre__icontains=texto) | Q(descripcion__icontains=texto)
        ).all()

        mensaje_busqueda = f"Se buscaron torneos que contienen en su nombre o contenido la palabra: {texto}"

        return render(request, 'torneo/formulario/buscar_torneo.html', {
            "torneos_mostrar": torneos,
            "texto_busqueda": mensaje_busqueda
        })
    
    # Si no se envió una búsqueda o la validación no fue correcta, redirigimos
    if "HTTP_REFERER" in request.META:
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect('index')"""
    
    
def torneo_buscar_avanzado(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaTorneoForm(request.GET)
        if formulario.is_valid():
            
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            
            QStorneos = Torneo.objects.all()
            
            # Obtenemos los filtros del formulario
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            fechaDesde = formulario.cleaned_data.get('fecha_desde')
            fechaHasta = formulario.cleaned_data.get('fecha_hasta')
            duracionMinima = formulario.cleaned_data.get('duracion_minima')
            
            # Por cada filtro comprobamos si tiene un valor y lo añadimos a la QuerySet
            if textoBusqueda != "":
                QStorneos = QStorneos.filter(Q(nombre__icontains=textoBusqueda) | Q(descripcion__icontains=textoBusqueda) |Q(categoria__contains=textoBusqueda))
                mensaje_busqueda += f" Nombre o contenido que contengan la palabra '{textoBusqueda}'\n"
            
            
            # Comprobamos las fechas
            if fechaDesde:
                mensaje_busqueda += f" Fecha desde: {fechaDesde.strftime('%d-%m-%Y')}\n"
                QStorneos = QStorneos.filter(fecha_inicio__gte=fechaDesde)
            
            if fechaHasta:
                mensaje_busqueda += f" Fecha hasta: {fechaHasta.strftime('%d-%m-%Y')}\n"
                QStorneos = QStorneos.filter(fecha_inicio__lte=fechaHasta)
            
            
            # Ejecutamos la consulta
            torneos = QStorneos.all()
    
            return render(request, 'torneo/formulario/buscar_torneo.html', {
                "torneos_mostrar": torneos,
                "texto_busqueda": mensaje_busqueda
            })
    else:
        formulario = BusquedaAvanzadaTorneoForm(None)
    
    return render(request, 'torneo/formulario/busqueda_avanzada_datepicker.html', {"formulario": formulario})




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

