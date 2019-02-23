from django import forms
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from events_manager.ticket.models import Event

class EventForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Datos Basicos',
                Row(
                    Div(
                        Field('name'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('descripcion'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('event_type'),
                        css_class='col-md-4'
                    )
                ),
                Row(
                    Div(
                        Field('capacity'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('date'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('division'),
                        css_class='col-md-4'
                    )
                ),
                Row(
                    Div(
                        Field('equipo_local'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('equipo_visitante'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('is_active'),
                        css_class='col-md-4'
                    )
                )             
            ),
            ButtonHolder(
                Submit('submit', 'Guardar', css_class='button white'),
                Button('cancel','Cancelar')
            )
        )
    def save(self, *args, **kwargs):
        return super(EventForm, self).save(*args, **kwargs)

    class Meta:
        model = Event
        fields = ['name','descripcion','event_type','capacity','date','division','equipo_local','equipo_visitante','is_active']
    
    