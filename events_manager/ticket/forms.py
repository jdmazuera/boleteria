from django import forms
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from events_manager.ticket.models import Ticket

class TicketForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = '#'
        self.helper.layout = Layout(
            Fieldset(
                'Datos Basicos',
                Row(
                    Div(
                        Field('receipt'),
                        css_class='col-md-3'
                    ),
                    Div(
                        Field('event_locality'),
                        css_class='col-md-3'
                    ),
                    Div(
                        Field('price'),
                        css_class='col-md-3'
                    ),
                    Div(
                        Field('quantity'),
                        css_class='col-md-3'
                    )               
                ),
                Row(
                    Div(
                        Field('tax'),
                        css_class='col-md-3'
                    ),
                    Div(
                        Field('subtotal'),
                        css_class='col-md-3'
                    ),
                    Div(
                        Field('total'),
                        css_class='col-md-3'
                    )
                )       
            ),
            ButtonHolder(
                Submit('submit', 'Guardar', css_class='button white'),
                HTML('<a class="btn btn-secondary" href={% url \'ticket:list\' %}>Cancelar</a></button>')
            )
        )

    def save(self, *args, **kwargs):
        return super(TicketForm, self).save(*args, **kwargs)

    class Meta:
        model = Ticket
        fields = ['receipt','event_locality','price','quantity','tax','subtotal','total']
    
    