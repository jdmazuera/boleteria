from django import forms
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from .models import *

class ReceiptForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReceiptForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = '#'
        self.helper.layout = Layout(
            Fieldset(
                'Datos Basicos',
                Row(
                    Div(
                        Field('salesman'),
                        css_class='col-md-3'
                    ),
                    Div(
                        Field('pay_method'),
                        css_class='col-md-3'
                    ),
                    Div(
                        Field('confirmed'),
                        css_class='col-md-3'
                    )                    
                )     
            ),
            ButtonHolder(
                Submit('submit', 'Guardar', css_class='button white'),
                HTML('<a class="btn btn-secondary" href={% url \'receipt:list\' %}>Cancelar</a></button>')
            )
        )

    def save(self, *args, **kwargs):
        return super(ReceiptForm, self).save(*args, **kwargs)

    class Meta:
        model = Receipt
        fields = ['salesman','pay_method','confirmed']
    
    