from django import forms
from .models import Torneo, Equipo, Participante
from django.utils import timezone
import datetime

class TorneoForm(forms.Form):
    # Campo para el nombre del torneo
    nombre = forms.CharField(label="Nombre del Torneo",
                             required=True, 
                             max_length=200,
                             help_text="200 caracteres como máximo")
    
    # Campo para la descripción del torneo
    descripcion = forms.CharField(label="Descripción del Torneo",
                                  required=False,
                                  widget=forms.Textarea())
    
    # Campo para la fecha de inicio del torneo
    fecha_inicio = forms.DateField(label="Fecha de Inicio",
                                   initial=datetime.date.today,
                                   widget=forms.SelectDateWidget())

    # Campo para la categoría del torneo
    categoria = forms.CharField(label="Categoría",
                                required=True,
                                max_length=100,
                                help_text="Categoría del torneo (por ejemplo, 'Acción', 'Deportes', etc.)")
    
    
    # Campo Select para seleccionar los participantes (relación ManyToMany)
    participantesDisponibles = Participante.objects.all()
    participantes = forms.ModelMultipleChoiceField(
        queryset=participantesDisponibles,
        required=True,
        widget=forms.CheckboxSelectMultiple,
        help_text="Selecciona los participantes del torneo"
    )
    
    # Campo para la duración del torneo
    duracion = forms.DurationField(label="Duración del Torneo",
                                   required=True,
                                   help_text="Duración del torneo en formato de tiempo (por ejemplo, '1:00:00' para 1 hora).")
