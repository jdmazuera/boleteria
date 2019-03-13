from django import forms
from django.forms import ModelForm,Form

from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from events_manager.event.models import Event

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
                        Field('event_type'),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('date'),
                        css_class='col-md-4'
                    )
                ),
                Row(
                    Div(
                        Field('descripcion'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('image_card'),
                        css_class='col-md-6'
                    )
                )             
            ),
            ButtonHolder(
                Submit('submit', 'Guardar', css_class='button white'),
                HTML('<a class="btn btn-secondary" href={% url \'event:list\' %}>Cancelar</a></button>')
            )
        )
    def save(self, *args, **kwargs):
        return super(EventForm, self).save(*args, **kwargs)

    class Meta:
        model = Event
        fields = ['name','descripcion','event_type','date','image_card']
    
    