from django import forms
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from events_manager.ticket.models import Ticket

class TicketForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
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
                        Field('price'),
                        css_class='col-md-6'
                    )
                ),
                Row(
                    Div(
                        Field('event'),
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
        return super(TicketForm, self).save(*args, **kwargs)

    class Meta:
        model = Ticket
        fields = ['name','price','event','date']
    
    