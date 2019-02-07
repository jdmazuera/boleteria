from django import forms
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from events_manager.event.models import Event

class EventForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        #self.fields['username'].widget.attrs.update({'class':'col-md-4'})
        #self.fields['email'].widget.attrs.update({'class':'col-md-4'})
        #self.fields['password'].widget.attrs.update({'class':'col-md-4'})
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Datos Basicos',
                Row(
                    Div(
                        Field('name'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('event_type'),
                        css_class='col-md-6'
                    )
                ),
                Row(
                    Div(
                        Field('capacity'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('date'),
                        css_class='col-md-6'
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
        fields = ['name','event_type','capacity','date']
    
    