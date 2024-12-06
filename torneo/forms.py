from django import forms  # Importa el módulo de formularios
from django.forms import ModelForm  # Importa ModelForm directamente
from .models import *
from datetime import datetime, date, timedelta
from django.forms import DateInput

class TorneoForm(forms.ModelForm):
    # Definimos los campos, aunque estos se tomarán directamente del modelo, así que puedes dejarlos como están si quieres personalizar algo.
    
    DURACIONES = [
        ('1:00', '1 hora'),
        ('2:00', '2 horas'),
        ('3:00', '3 horas'),
        ('4:00', '4 horas'),
        ('5:00', '5 horas'),
        ('6:00', '6 horas'),
        ('12:00', '12 horas'),
        ('24:00', '1 día'),
    ]

    CATEGORIAS = [
        ('Acción', 'Acción'),
        ('Deportes', 'Deportes'),
        ('Aventura', 'Aventura'),
        ('Estrategia', 'Estrategia'),
    ]
    
    categoria = forms.ChoiceField(
        label="Categoría",
        choices=CATEGORIAS,
        required=True,
        help_text="Selecciona la categoría del torneo (por ejemplo, 'Acción', 'Deportes', etc.)"
    )
    
    participantes = forms.ModelMultipleChoiceField(
        queryset=Participante.objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple(),
        help_text="Selecciona los participantes del torneo"
    )
    
    duracion = forms.ChoiceField(
        label="Duración del Torneo",
        choices=DURACIONES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Selecciona la duración del torneo"
    )
    
    class Meta:
        model = Torneo  # Asociamos el formulario al modelo Torneo
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'categoria', 'participantes', 'duracion']  # Campos que se mostrarán en el formulario

    def clean(self):
        super().clean() #se llama al clean ejecutan las validaciones 
        #predefinidas de Django (como asegurarse de que los campos requeridos estén presentes, que los campos numéricos sean válidos, etc.), 
        #y luego se devuelve un diccionario cleaned_data con los valores validados de los campos.

        #una vez calidado accedes a los valores del clean y ya luego podemos añadir nuestros propios errores
        nombre = self.cleaned_data.get('nombre')
        descripcion = self.cleaned_data.get('descripcion')
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        categoria = self.cleaned_data.get('categoria')
        participantes = self.cleaned_data.get('participantes')
        duracion = self.cleaned_data.get('duracion')
        
            # Asegurarnos de que duracion esté en formato timedelta
        if isinstance(duracion, str):  # Si la duración es una cadena de texto, la convertimos a timedelta
            horas, minutos = map(int, duracion.split(':'))
            duracion = timedelta(hours=horas, minutes=minutos)

        # Validaciones personalizadas (como las tenías)
        torneo_existente = Torneo.objects.filter(nombre=nombre).first()
        if torneo_existente:
            self.add_error('nombre', 'Ya existe un torneo con ese nombre.')

        if descripcion and len(descripcion) < 20:
            self.add_error('descripcion', 'La descripción debe tener al menos 20 caracteres.')

        if fecha_inicio and fecha_inicio < date.today():
            self.add_error('fecha_inicio', 'La fecha de inicio no puede ser anterior a hoy.')
        # Comprobamos que la categoría sea 'Acción' y que la duración supere las 3 horas (10800 segundos)
        if categoria and categoria.lower() == "acción":
            if duracion:
                # Verifica si la duración es mayor a 3 horas (10800 segundos)
                if isinstance(duracion, timedelta) and duracion.total_seconds() > 10800:
                    self.add_error('categoria', 'La categoría "Acción" no puede tener una duración superior a 3 horas.')
                    self.add_error('duracion', 'Duración no válida para la categoría "Acción".')

                return self.cleaned_data


        if participantes and len(participantes) < 2:
            self.add_error('participantes', 'Debe seleccionar al menos dos participantes.')

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
        super().clean()

        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        fecha_ingreso_desde = self.cleaned_data.get('fecha_ingreso_desde')
        fecha_ingreso_hasta = self.cleaned_data.get('fecha_ingreso_hasta')
        puntos_minimos = self.cleaned_data.get('puntos_minimos')
        puntos_maximos = self.cleaned_data.get('puntos_maximos')

        if not (textoBusqueda and fecha_ingreso_desde and fecha_ingreso_hasta and puntos_minimos and puntos_maximos):
            self.add_error('textoBusqueda', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_ingreso_desde', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_ingreso_hasta', 'Debe introducir al menos un valor en un campo del formulario')

        if textoBusqueda and len(textoBusqueda) < 3:
            self.add_error('textoBusqueda', 'Debe introducir al menos 3 caracteres')

        if fecha_ingreso_desde and fecha_ingreso_hasta and fecha_ingreso_hasta < fecha_ingreso_desde:
            self.add_error('fecha_ingreso_hasta', 'La fecha "hasta" no puede ser menor que la fecha "desde"')

        if puntos_minimos is not None and puntos_maximos is not None:
            if puntos_minimos > puntos_maximos:
                self.add_error('puntos_minimos', 'Los puntos mínimos no pueden ser mayores que los puntos máximos')
                self.add_error('puntos_maximos', 'Los puntos máximos no pueden ser menores que los puntos mínimos')
        return self.cleaned_data



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
    
    
class BusquedaParticipanteForm(forms.Form):
    textoBusqueda = forms.CharField(required=False)

class BusquedaAvanzadaParticipanteForm(forms.Form):
    textoBusqueda = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del participante'}),
        label="Nombre del Participante"
    )
    fecha_inscripcion_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Fecha de inscripción desde"
    )
    fecha_inscripcion_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Fecha de inscripción hasta"
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
    tiempo_jugado_minimo = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Tiempo jugado mínimo (en horas)"
    )
    tiempo_jugado_maximo = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Tiempo jugado máximo (en horas)"
    )

    def clean(self):
        super().clean()

        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        fecha_inscripcion_desde = self.cleaned_data.get('fecha_inscripcion_desde')
        fecha_inscripcion_hasta = self.cleaned_data.get('fecha_inscripcion_hasta')
        puntos_minimos = self.cleaned_data.get('puntos_minimos')
        puntos_maximos = self.cleaned_data.get('puntos_maximos')
        tiempo_jugado_minimo = self.cleaned_data.get('tiempo_jugado_minimo')
        tiempo_jugado_maximo = self.cleaned_data.get('tiempo_jugado_maximo')

        # Validación: Al menos un campo debe estar lleno
        if not (textoBusqueda or fecha_inscripcion_desde or fecha_inscripcion_hasta or puntos_minimos or puntos_maximos or tiempo_jugado_minimo or tiempo_jugado_maximo):
            self.add_error('textoBusqueda', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_inscripcion_desde', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_inscripcion_hasta', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('puntos_minimos', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('puntos_maximos', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('tiempo_jugado_minimo', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('tiempo_jugado_maximo', 'Debe introducir al menos un valor en un campo del formulario')

        # Validación: La fecha "hasta" no puede ser menor que la fecha "desde"
        if fecha_inscripcion_desde and fecha_inscripcion_hasta and fecha_inscripcion_hasta < fecha_inscripcion_desde:
            self.add_error('fecha_inscripcion_hasta', 'La fecha "hasta" no puede ser anterior a la fecha "desde"')

        # Validación: Los puntos mínimos no pueden ser mayores que los máximos
        if puntos_minimos is not None and puntos_maximos is not None and puntos_minimos > puntos_maximos:
            self.add_error('puntos_minimos', 'Los puntos mínimos no pueden ser mayores que los puntos máximos')
            self.add_error('puntos_maximos', 'Los puntos máximos no pueden ser menores que los puntos mínimos')

        # Validación: El tiempo jugado mínimo no puede ser mayor que el máximo
        if tiempo_jugado_minimo is not None and tiempo_jugado_maximo is not None and tiempo_jugado_minimo > tiempo_jugado_maximo:
            self.add_error('tiempo_jugado_minimo', 'El tiempo jugado mínimo no puede ser mayor que el tiempo jugado máximo')
            self.add_error('tiempo_jugado_maximo', 'El tiempo jugado máximo no puede ser menor que el tiempo jugado mínimo')

        return self.cleaned_data
    

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario  # Modelo asociado al formulario
        fields = ['nombre', 'correo', 'clave_de_acceso', 'fecha_registro']  # Campos a incluir en el formulario
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'clave_de_acceso': forms.PasswordInput(attrs={'class': 'form-control'}),
            'fecha_registro': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
        labels = {
            'nombre': "Nombre del Usuario",
            'correo': "Correo Electrónico",
            'clave_de_acceso': "Clave de Acceso",
            'fecha_registro': "Fecha de Registro",
        }
        help_texts = {
            'nombre': "Nombre completo del usuario",
            'correo': "Correo electrónico único para el usuario",
            'clave_de_acceso': "Una clave segura para acceder al sistema",
            'fecha_registro': "Fecha y hora en que se registró el usuario",
        }

    def clean(self):
        # Validamos con el modelo actual
        super().clean()

        # Obtenemos los campos
        correo = self.cleaned_data.get('correo')
        clave_de_acceso = self.cleaned_data.get('clave_de_acceso')

        # Comprobamos si el correo ya está registrado
        usuario_existente = Usuario.objects.filter(correo=correo).first()
        if usuario_existente:
            if self.instance and usuario_existente.id == self.instance.id:
                pass
            else:
                self.add_error('correo', 'Ya existe un usuario con ese correo electrónico.')

        # Comprobamos que la clave de acceso tenga al menos 8 caracteres
        if clave_de_acceso and len(clave_de_acceso) < 8:
            self.add_error('clave_de_acceso', 'La clave de acceso debe tener al menos 8 caracteres.')

        # Siempre devolvemos el conjunto de datos
        return self.cleaned_data
    
    

class BusquedaUsuarioForm(forms.Form):
    textoBusqueda = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre o correo del usuario'}), label="Nombre o Correo del Usuario")

    fecha_registro_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Fecha de registro desde"
    )
    fecha_registro_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Fecha de registro hasta"
    )

    def clean(self):
        super().clean()

        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        fecha_registro_desde = self.cleaned_data.get('fecha_registro_desde')
        fecha_registro_hasta = self.cleaned_data.get('fecha_registro_hasta')

        # Validación: Al menos un campo debe estar lleno
        if not (textoBusqueda or fecha_registro_desde or fecha_registro_hasta):
            self.add_error('textoBusqueda', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_registro_desde', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_registro_hasta', 'Debe introducir al menos un valor en un campo del formulario')

        # Validación: La fecha "hasta" no puede ser menor que la fecha "desde"
        if fecha_registro_desde and fecha_registro_hasta and fecha_registro_hasta < fecha_registro_desde:
            self.add_error('fecha_registro_hasta', 'La fecha "hasta" no puede ser anterior a la fecha "desde"')

        return self.cleaned_data
    
    
    
class JuegoForm(forms.ModelForm):
    class Meta:
        model = Juego  # Modelo asociado al formulario
        fields = ['nombre', 'genero', 'id_consola', 'descripcion', 'torneo']  # Campos a incluir en el formulario
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'torneo': forms.Select(attrs={'class': 'form-control'}),
            'id_consola': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre': "Nombre del Juego",
            'genero': "Género del Juego",
            'descripcion': "Descripción del Juego",
            'torneo': "Torneo Asociado",
            'id_consola': "Consola",
        }
        help_texts = {
            'nombre': "Nombre del juego",
            'genero': "Género del juego (acción, aventura, etc.)",
            'descripcion': "Descripción breve del juego",
            'torneo': "Torneo al que está asociado el juego",
            'id_consola': "Consola en la que se juega",
        }

    def clean(self):
        # Validamos con el modelo actual
        super().clean()

        # Obtenemos los campos
        nombre = self.cleaned_data.get('nombre')

        # Comprobamos si el nombre del juego ya está registrado
        juego_existente = Juego.objects.filter(nombre=nombre).first()
        if juego_existente:
            if self.instance and juego_existente.id == self.instance.id:
                pass
            else:
                self.add_error('nombre', 'Ya existe un juego con ese nombre.')

        # Siempre devolvemos el conjunto de datos
        return self.cleaned_data


class BusquedaJuegoForm(forms.Form):
    nombre = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del juego'}),
        label="Nombre del Juego"
    )

    genero = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Género del juego'}),
        label="Género"
    )

    fecha_creacion_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Fecha de creación desde"
    )

    fecha_creacion_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Fecha de creación hasta"
    )

    def clean(self):
        super().clean()

        nombre = self.cleaned_data.get('nombre')
        genero = self.cleaned_data.get('genero')
        fecha_creacion_desde = self.cleaned_data.get('fecha_creacion_desde')
        fecha_creacion_hasta = self.cleaned_data.get('fecha_creacion_hasta')

        # Validación: Al menos un campo debe estar lleno
        if not (nombre or genero or fecha_creacion_desde or fecha_creacion_hasta):
            self.add_error('nombre', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('genero', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_creacion_desde', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_creacion_hasta', 'Debe introducir al menos un valor en un campo del formulario')

        # Validación: La fecha "hasta" no puede ser menor que la fecha "desde"
        if fecha_creacion_desde and fecha_creacion_hasta and fecha_creacion_hasta < fecha_creacion_desde:
            self.add_error('fecha_creacion_hasta', 'La fecha "hasta" no puede ser anterior a la fecha "desde"')

        return self.cleaned_data
    
    
class PerfilDeJugadorForm(forms.ModelForm):
    class Meta:
        model = PerfilDeJugador
        fields = ['usuario', 'puntos', 'nivel', 'ranking', 'avatar']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'puntos': forms.NumberInput(attrs={'class': 'form-control'}),
            'nivel': forms.NumberInput(attrs={'class': 'form-control'}),
            'ranking': forms.NumberInput(attrs={'class': 'form-control'}),
            'avatar': forms.URLInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'usuario': "Usuario",
            'puntos': "Puntos",
            'nivel': "Nivel",
            'ranking': "Ranking",
            'avatar': "Avatar (URL)",
        }
        help_texts = {
            'usuario': "Selecciona el usuario del jugador.",
            'puntos': "Puntos acumulados por el jugador.",
            'nivel': "Nivel del jugador.",
            'ranking': "Ranking del jugador.",
            'avatar': "URL de la imagen del avatar del jugador.",
        }

    def clean(self):
        # Llamamos al método clean() de la clase base
        super().clean()

        # Obtenemos los campos
        usuario = self.cleaned_data.get('usuario')
        puntos = self.cleaned_data.get('puntos')
        nivel = self.cleaned_data.get('nivel')
        ranking = self.cleaned_data.get('ranking')
        avatar = self.cleaned_data.get('avatar')

        # Validar que el usuario no esté vacío ni solo contenga espacios
        if not usuario:
            self.add_error('usuario', 'El usuario es obligatorio.')

        # Validación de unicidad del usuario
        perfil_existente = PerfilDeJugador.objects.filter(usuario=usuario).first()
        if perfil_existente:
            if self.instance and perfil_existente.id == self.instance.id:
                pass
            else:
                self.add_error('usuario', 'Este usuario ya tiene un perfil de jugador.')

        # Validar que los puntos, nivel y ranking sean valores positivos
        if puntos is not None and puntos < 0:
            self.add_error('puntos', 'Los puntos deben ser un valor positivo.')
        if nivel is not None and nivel < 0:
            self.add_error('nivel', 'El nivel debe ser un valor positivo.')
        if ranking is not None and ranking < 0:
            self.add_error('ranking', 'El ranking debe ser un valor positivo.')

        # Validar que el avatar sea una URL válida
        if avatar and not avatar.startswith(('http://', 'https://')):
            self.add_error('avatar', 'El avatar debe ser una URL válida.')

        # Siempre devolvemos el conjunto de datos limpios
        return self.cleaned_data
    
    
class BusquedaPerfilJugadorForm(forms.Form):
    textoBusqueda = forms.CharField(required=False)

class BusquedaAvanzadaPerfilJugadorForm(forms.Form):
    textoBusqueda = forms.CharField(required=False)
    
    # Campo para filtrar por puntos
    puntos_minimos = forms.IntegerField(
        label="Puntos Mínimos", 
        required=False, 
        widget=forms.NumberInput(attrs={'placeholder': 'Introduce los puntos mínimos'})
    )

    nivel_minimo = forms.IntegerField(
        label="Nivel Mínimo", 
        required=False, 
        widget=forms.NumberInput(attrs={'placeholder': 'Introduce el nivel mínimo'})
    )

    # Fecha de creación del perfil (si la tienes en el modelo)
    fecha_desde = forms.DateField(
        label="Fecha Desde", 
        required=False, 
        widget=DateInput(attrs={"type": "date", "class": "form-control"})
    )

    fecha_hasta = forms.DateField(
        label="Fecha Hasta", 
        required=False, 
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"})
    )

    def clean(self):
        super().clean()

        # Obtenemos los campos
        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        puntos_minimos = self.cleaned_data.get('puntos_minimos')
        nivel_minimo = self.cleaned_data.get('nivel_minimo')
        fecha_desde = self.cleaned_data.get('fecha_desde')
        fecha_hasta = self.cleaned_data.get('fecha_hasta')

        # Validar que al menos uno de los campos tenga un valor
        if textoBusqueda == "" and puntos_minimos is None and nivel_minimo is None and fecha_desde is None and fecha_hasta is None:
            self.add_error('textoBusqueda', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('puntos_minimos', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('nivel_minimo', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_desde', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_hasta', 'Debe introducir al menos un valor en un campo del formulario')

        # Validar que el texto de búsqueda tenga al menos 3 caracteres si se ingresa algo
        if textoBusqueda != "" and len(textoBusqueda) < 3:
            self.add_error('textoBusqueda', 'Debe introducir al menos 3 caracteres')

        # La fecha hasta debe ser mayor o igual a la fecha desde
        if fecha_desde and fecha_hasta and fecha_hasta < fecha_desde:
            self.add_error('fecha_desde', 'La fecha hasta no puede ser menor que la fecha desde')
            self.add_error('fecha_hasta', 'La fecha hasta no puede ser menor que la fecha desde')

        # Validar que los puntos y el nivel sean mayores a cero si se ingresan
        if puntos_minimos is not None and puntos_minimos < 0:
            self.add_error('puntos_minimos', 'Los puntos deben ser un valor mayor o igual a cero')

        if nivel_minimo is not None and nivel_minimo < 0:
            self.add_error('nivel_minimo', 'El nivel debe ser un valor mayor o igual a cero')

        return self.cleaned_data





    



   
