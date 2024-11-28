from django import forms  # Importa el módulo de formularios
from django.forms import ModelForm  # Importa ModelForm directamente
from .models import *
from datetime import datetime, date
from django.forms import DateInput




class TorneoForm(forms.ModelForm):
    class Meta:
        model = Torneo  # Modelo asociado al formulario
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'categoria', 'participantes', 'duracion']  # Campos a incluir en el formulario
        widgets = {
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'participantes': forms.CheckboxSelectMultiple(),
            'duracion': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
        labels = {
            'nombre': "Nombre del Torneo",
            'descripcion': "Descripción del Torneo",
            'fecha_inicio': "Fecha de Inicio",
            'categoria': "Categoría",
            'participantes': "Participantes",
            'duracion': "Duración del Torneo",
        }
        help_texts = {
            'nombre': "200 caracteres como máximo",
            'categoria': "Categoría del torneo (por ejemplo, 'Acción', 'Deportes', etc.)",
            'participantes': "Selecciona los participantes del torneo",
            'duracion': "Duración del torneo en formato de tiempo (por ejemplo, '1:00:00' para 1 hora).",
        }
    
    def clean(self):
        # Validamos con el modelo actual
        super().clean()

        # Obtenemos los campos
        nombre = self.cleaned_data.get('nombre')
        descripcion = self.cleaned_data.get('descripcion')
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        categoria = self.cleaned_data.get('categoria')
        participantes = self.cleaned_data.get('participantes')
        duracion = self.cleaned_data.get('duracion')

        # Comprobamos que no exista un torneo con ese nombre
        torneo_existente = Torneo.objects.filter(nombre=nombre).first()
        if torneo_existente:
            if self.instance and torneo_existente.id == self.instance.id:
                pass
            else:
                self.add_error('nombre', 'Ya existe un torneo con ese nombre.')

        # Comprobamos que la descripción tenga al menos 20 caracteres
        if descripcion and len(descripcion) < 20:
            self.add_error('descripcion', 'La descripción debe tener al menos 20 caracteres.')

        # Comprobamos que la fecha de inicio no sea anterior a hoy
        if fecha_inicio and fecha_inicio < date.today():
            self.add_error('fecha_inicio', 'La fecha de inicio no puede ser anterior a hoy.')

        # Comprobamos que la categoría no sea "Infantil" si la duración supera las 3 horas
        if categoria: 
         if categoria.lower() == "Executive also relate family." and duracion and duracion.total_seconds() > 10800:
                self.add_error('categoria', 'La categoría "Executive also relate family." no puede tener una duración superior a 3 horas.')
                self.add_error('duracion', 'Duración no válida para la categoría "Executive also relate family.".')

        # Comprobamos que haya al menos 2 participantes seleccionados
        if participantes and len(participantes) < 2:
            self.add_error('participantes', 'Debe seleccionar al menos dos participantes.')

        # Siempre devolvemos el conjunto de datos
        return self.cleaned_data
    
    
class BusquedaTorneoForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    
    
class BusquedaAvanzadaTorneoForm(forms.Form):
    textoBusqueda = forms.CharField(required=False)
    
    # Supongo que tienes una lista de categorías o algo similar en tu modelo de Torneo
    categorias = forms.CharField(
    required=False,
    widget=forms.TextInput(attrs={'placeholder': 'Introduce las categorías separadas por comas'})
)

    fecha_desde = forms.DateField(label="Fecha Desde", 
                                  required=False, 
                                  widget=DateInput(attrs={"type": "date", "class": "form-control"}))

    fecha_hasta = forms.DateField(label="Fecha Hasta", 
                                  required=False, 
                                  widget=forms.DateInput(format="%Y-%m-%d", 
                                                         attrs={"type": "date", "class": "form-control"}))

    # Filtrar por duración mínima de los torneos
    duracion_minima = forms.TimeField(label="Duración mínima", 
                                      required=False, 
                                      widget=forms.TimeInput(attrs={"type": "time", "class": "form-control"}))

    def clean(self):
        # Validamos con el formulario base
        super().clean()

        # Obtenemos los campos
        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        categorias = self.cleaned_data.get('categorias')
        fecha_desde = self.cleaned_data.get('fecha_desde')
        fecha_hasta = self.cleaned_data.get('fecha_hasta')
        duracion_minima = self.cleaned_data.get('duracion_minima')

        # Controlamos que al menos se haya introducido un valor en uno de los campos
        if textoBusqueda == "" and len(categorias) == 0 and fecha_desde is None and fecha_hasta is None and duracion_minima is None:
            self.add_error('textoBusqueda', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('categorias', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_desde', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_hasta', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('duracion_minima', 'Debe introducir al menos un valor en un campo del formulario')
        else:
            # Validar que el texto de búsqueda tenga al menos 3 caracteres si se ingresa algo
            if textoBusqueda != "" and len(textoBusqueda) < 3:
                self.add_error('textoBusqueda', 'Debe introducir al menos 3 caracteres')

            # La fecha hasta debe ser mayor o igual a la fecha desde, si ambas se introducen
            if fecha_desde and fecha_hasta and fecha_hasta < fecha_desde:
                self.add_error('fecha_desde', 'La fecha hasta no puede ser menor que la fecha desde')
                self.add_error('fecha_hasta', 'La fecha hasta no puede ser menor que la fecha desde')

            # Si se especifica una duración mínima, debe ser un tiempo positivo
            if duracion_minima:
                if duracion_minima.total_seconds() <= 0:
                    self.add_error('duracion_minima', 'La duración mínima debe ser un tiempo válido y mayor que cero')

        # Siempre devolvemos el conjunto de datos
        return self.cleaned_data

class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['nombre', 'logotipo', 'fecha_ingreso', 'puntos_contribuidos']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce el nombre del equipo'}),
            'logotipo': forms.URLInput(attrs={'class': 'form-control'}),
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'puntos_contribuidos': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre': "Nombre del Equipo",
            'logotipo': "URL del Logotipo",
            'fecha_ingreso': "Fecha de Ingreso",
            'puntos_contribuidos': "Puntos Contribuidos",
        }
        help_texts = {
            'nombre': "Máximo 200 caracteres.",
            'logotipo': "URL de la imagen del logotipo del equipo.",
            'fecha_ingreso': "Fecha en que el equipo se unió.",
            'puntos_contribuidos': "Puntos que el equipo ha contribuido en total.",
        }

    def clean(self):
        # Llamada al método clean() de la clase base
        cleaned_data = super().clean()

        # Acceder a los valores de los campos limpios
        nombre = cleaned_data.get('nombre')
        puntos_contribuidos = cleaned_data.get('puntos_contribuidos')

        # Validar que el nombre no esté vacío ni solo contenga espacios
        if not nombre or not nombre.strip():
            self.add_error('nombre', 'El nombre del equipo es obligatorio.')

        # Validación de unicidad del nombre
        if nombre and Equipo.objects.filter(nombre=nombre).exclude(id=self.instance.id).exists():
            self.add_error('nombre', 'Ya existe un equipo con ese nombre.')

        # Validar que los puntos contribuidos sean positivos
        if puntos_contribuidos is not None and puntos_contribuidos < 0:
            self.add_error('puntos_contribuidos', 'Los puntos contribuidos deben ser un valor positivo.')

        return cleaned_data



    



   
