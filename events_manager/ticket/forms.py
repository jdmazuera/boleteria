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
                        Field('event'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('price'),
                        css_class='col-md-6'
                    )
                ),
                Row(
                    Div(
                        Field('date'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('propietario'),
                        css_class='col-md-6'
                    )
                ),
                Row(
                    Div(
                        Field('estado'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('metodo_pago'),
                        css_class='col-md-6'
                    )
                )         
            ),
            ButtonHolder(
                Submit('submit', 'Comprar', css_class='button white'),
                HTML('<a class="btn btn-secondary" href={% url \'event:list\' %}>Cancelar</a></button>')
            )
        )

    def save(self, *args, **kwargs):
        return super(TicketForm, self).save(*args, **kwargs)

    class Meta:
        model = Ticket
        fields = ['price']
    
    