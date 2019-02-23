from django import forms
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from events_manager.core.models import User

class UserFrom(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserFrom, self).__init__(*args, **kwargs)
        #self.fields['username'].widget.attrs.update({'class':'col-md-4'})
        #self.fields['email'].widget.attrs.update({'class':'col-md-4'})
        #self.fields['password'].widget.attrs.update({'class':'col-md-4'})
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Datos Basicos',
                Row(
                    Div(
                        Field('username'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('identification'),
                        css_class='col-md-6'
                    )
                ),
                Row(
                    Div(
                        Field('first_name'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('last_name'),
                        css_class='col-md-6'
                    )
                ),
                Row(
                    Div(
                        Field('password'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('email'),
                        css_class='col-md-6'
                    )
                )                 
            ),
            Fieldset(
                'Datos De Contacto',
                Row(
                    Div(
                        Field('address'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('position'),
                        css_class='col-md-6'
                    )
                ),
                Row(
                    Div(
                        Field('phone'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('mobile'),
                        css_class='col-md-6'
                    )
                ),
                Row(
                    Div(
                        Field('is_active'),
                        css_class='col-md-6'
                    )
                )               
            ),
            ButtonHolder(
                Submit('submit', 'Guardar', css_class='button white'),
                HTML('<a class="btn btn-secondary" href={% url \'core:list\' %}>Cancelar</a></button>')
            )
        )
        self.fields['password'] = forms.CharField(widget=forms.PasswordInput)

    def save(self, *args, **kwargs):
        self.instance.set_password(self.instance.password)
        return super(UserFrom, self).save(*args, **kwargs)

    class Meta:
        model = User
        fields = ['username','first_name','last_name','identification','email','password','address','position','phone','mobile','is_active']

class RegistroForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Fieldset(
                None,
                Field('username'),
                Field('identification'),
                Field('first_name'),
                Field('last_name'),
                Field('email'),
                Field('password')
            ),
            ButtonHolder(
                Submit('submit', 'Guardar', css_class='button white'),
                HTML('<a class="btn btn-secondary" href={% url \'core:login\' %}>Cancelar</a></button>')
            )
        )

        self.fields['password'] = forms.CharField(widget=forms.PasswordInput)
    
    def save(self, *args, **kwargs):
        self.instance.set_password(self.instance.password)
        return super(RegistroForm, self).save(*args, **kwargs)
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','identification','email','password','address','position','phone','mobile']