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
        # Llamamos al método clean() de la clase base
        super().clean()

        # Obtenemos los campos
        nombre = self.cleaned_data.get('nombre')
        logotipo = self.cleaned_data.get('logotipo')
        fecha_ingreso = self.cleaned_data.get('fecha_ingreso')
        puntos_contribuidos = self.cleaned_data.get('puntos_contribuidos')

        # Validar que el nombre no esté vacío ni solo contenga espacios
        if not nombre or not nombre.strip():
            self.add_error('nombre', 'El nombre del equipo es obligatorio.')

        # Validación de unicidad del nombre
        equipo_existente = Equipo.objects.filter(nombre=nombre).first()
        if equipo_existente:
            if self.instance and equipo_existente.id == self.instance.id:
                pass
            else:
                self.add_error('nombre', 'Ya existe un equipo con ese nombre.')

        # Validar que el logotipo sea una URL válida (opcional si no es obligatorio)
        if logotipo and not logotipo.startswith(('http://', 'https://')):
            self.add_error('logotipo', 'El logotipo debe ser una URL válida.')

        # Validar que la fecha de ingreso no sea futura
        if fecha_ingreso and fecha_ingreso > date.today():
            self.add_error('fecha_ingreso', 'La fecha de ingreso no puede ser futura.')

        # Validar que los puntos contribuidos sean positivos
        if puntos_contribuidos is not None and puntos_contribuidos < 0:
            self.add_error('puntos_contribuidos', 'Los puntos contribuidos deben ser un valor positivo.')

        # Siempre devolvemos el conjunto de datos limpios
        return self.cleaned_data


class BusquedaEquipoForm(forms.Form):
    textoBusqueda = forms.CharField(required=False)

class BusquedaAvanzadaEquipoForm(forms.Form):
    textoBusqueda = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del equipo'}),
        label="Nombre"
    )
    fecha_ingreso_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Fecha de ingreso desde"
    )
    fecha_ingreso_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Fecha de ingreso hasta"
    )
    puntos_minimos = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Puntos mínimos"
    )
    puntos_maximos = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Puntos máximos"
    )


    def clean(self):
        # Misma lógica de validación que antes
        cleaned_data = super().clean()

        textoBusqueda = cleaned_data.get('textoBusqueda')
        fecha_ingreso_desde = cleaned_data.get('fecha_ingreso_desde')
        fecha_ingreso_hasta = cleaned_data.get('fecha_ingreso_hasta')
        puntos_minimos = cleaned_data.get('puntos_minimos')
        puntos_maximos = cleaned_data.get('puntos_maximos')

        if not (textoBusqueda or fecha_ingreso_desde or fecha_ingreso_hasta or puntos_minimos or puntos_maximos):
            self.add_error(None, 'Debe introducir al menos un valor en un campo del formulario')

        if textoBusqueda and len(textoBusqueda) < 3:
            self.add_error('textoBusqueda', 'Debe introducir al menos 3 caracteres')

        if fecha_ingreso_desde and fecha_ingreso_hasta and fecha_ingreso_hasta < fecha_ingreso_desde:
            self.add_error('fecha_ingreso_hasta', 'La fecha "hasta" no puede ser menor que la fecha "desde"')

        if puntos_minimos is not None and puntos_maximos is not None:
            if puntos_minimos > puntos_maximos:
                self.add_error('puntos_minimos', 'Los puntos mínimos no pueden ser mayores que los puntos máximos')
                self.add_error('puntos_maximos', 'Los puntos máximos no pueden ser menores que los puntos mínimos')
        return cleaned_data



class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante  # Modelo asociado al formulario
        fields = ['usuario', 'puntos_obtenidos', 'posicion_final', 'fecha_inscripcion', 'tiempo_jugado', 'equipos']  # Campos a incluir en el formulario
        widgets = {
            'fecha_inscripcion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'equipos': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'usuario': "Usuario",
            'puntos_obtenidos': "Puntos Obtenidos",
            'posicion_final': "Posición Final",
            'fecha_inscripcion': "Fecha de Inscripción",
            'tiempo_jugado': "Tiempo Jugado (horas)",
            'equipos': "Equipos",
        }
        help_texts = {
            'puntos_obtenidos': "Puntos obtenidos en el torneo.",
            'posicion_final': "Posición en la que terminó el participante.",
            'tiempo_jugado': "El tiempo total jugado por el participante en horas.",
            'equipos': "Selecciona los equipos a los que pertenece el participante.",
        }

    def clean(self):
        # Validamos con el modelo actual
        super().clean()

        # Obtenemos los campos
        usuario = self.cleaned_data.get('usuario')
        puntos_obtenidos = self.cleaned_data.get('puntos_obtenidos')
        posicion_final = self.cleaned_data.get('posicion_final')
        fecha_inscripcion = self.cleaned_data.get('fecha_inscripcion')
        tiempo_jugado = self.cleaned_data.get('tiempo_jugado')
        equipos = self.cleaned_data.get('equipos')

        # Comprobamos que el usuario no esté registrado como participante
        participante_existente = Participante.objects.filter(usuario=usuario).first()
        if participante_existente:
            if self.instance and participante_existente.id == self.instance.id:
                pass
            else:
                self.add_error('usuario', 'Este usuario ya está registrado como participante.')

        # Comprobamos que los puntos obtenidos sean positivos
        if puntos_obtenidos is not None and puntos_obtenidos < 0:
            self.add_error('puntos_obtenidos', 'Los puntos obtenidos no pueden ser negativos.')

        # Comprobamos que la posición final sea un número positivo
        if posicion_final is not None and posicion_final < 1:
            self.add_error('posicion_final', 'La posición final debe ser un número positivo.')

        # Comprobamos que el tiempo jugado no sea negativo
        if tiempo_jugado is not None and tiempo_jugado < 0:
            self.add_error('tiempo_jugado', 'El tiempo jugado no puede ser negativo.')

        # Comprobamos que al menos un equipo esté seleccionado
        if not equipos:
            self.add_error('equipos', 'Debe seleccionar al menos un equipo para el participante.')

        # Siempre devolvemos el conjunto de datos
        return self.cleaned_data



    



   
