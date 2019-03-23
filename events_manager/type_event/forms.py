from django import forms
from django.forms import ModelForm,Form

from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from events_manager.type_event.models import TypeEvent

class TypeEventForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TypeEventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = '#'
        self.helper.layout = Layout(
            Fieldset(
                'Datos Basicos',
                Row(
                    Div(
                        Field('name'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('description'),
                        css_class='col-md-6'
                    )
                )           
            ),
            ButtonHolder(
                Submit('submit', 'Guardar', css_class='button white'),
                HTML('<a class="btn btn-secondary" href={% url \'type_event:list\' %}>Cancelar</a></button>')
            )
        )
    def save(self, *args, **kwargs):
        return super(TypeEventForm, self).save(*args, **kwargs)

    class Meta:
        model = TypeEvent
        fields = ['name','description']
    