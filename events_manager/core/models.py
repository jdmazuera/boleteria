from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    POSITIONS = (
        ('Asesor','Asesor'),
        ('Odontologo','Odontologo')
    )

    identification = models.CharField(max_length=40,blank=False,null=False,default='',verbose_name='Identificación')
    address = models.CharField(max_length=255,blank=True,null=True,verbose_name='Dirección')
    position = models.CharField(max_length=100,choices=POSITIONS,blank=True,null=True,verbose_name='Cargo')
    phone = models.CharField(max_length=40,blank=True,null=True,verbose_name='Telefono')
    mobile = models.CharField(max_length=40,blank=True,null=True,verbose_name='Celular')
    

    def __str__(self):
        return self.email

User._meta.get_field('username').verbose_name = 'Nombre De Usuario'
User._meta.get_field('email').verbose_name = 'Correo Electronico'