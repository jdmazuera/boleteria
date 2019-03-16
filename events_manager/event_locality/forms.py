from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from events_manager.event_locality.models import EventLocality

class EventLocalityForm(forms.Form):
    def __init__(self,event,*args, **kwargs):
        super(EventLocalityForm, self).__init__(*args, **kwargs)
        self.event = event
        self.helper = FormHelper()
        self.helper.layout = Layout()

        self.helper.layout = Layout()

        self.helper.layout.append(Fieldset('Localidades'))

        localities = event.event_type.event_type_locality.all()

        for locality in localities:
            self.fields[str(locality.id)] = forms.CharField(label='Nombre Localidad',initial=locality.name,disabled=True)
            self.fields[str(locality.id)+'_capacity'] = forms.IntegerField(label='Capacidad',min_value=1)
            self.fields[str(locality.id)+'_price'] = forms.IntegerField(label='Precio',min_value=1)
            self.helper.layout[0].append(
                Row(
                    Div(
                        Field(str(locality.id)),
                        css_class='col-xs-4 col-sm-4 col-md-4 col-lg-2'
                    ),
                    Div(
                        Field(str(locality.id)+'_capacity'),
                        css_class='col-xs-4 col-sm-4 col-md-4 col-lg-2'
                    ),
                    Div(
                        Field(str(locality.id)+'_price'),
                        css_class='col-xs-4 col-sm-4 col-md-4 col-lg-2'
                    )
                )
            )

        self.helper.layout[0].append(
            ButtonHolder(
                Submit('submit', 'Guardar', css_class='button white'),
                HTML('<a class="btn btn-secondary" href={% url \'event:list\' %}>Cancelar</a></button>')
            )
        )
    def save(self,*args, **kwargs):
        print(self.fields)

        
        
        