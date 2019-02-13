from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    POSITIONS = (
        ('Vendedor','Vendedor'),
        ('Cliente','Cliente'),
        ('Administrador Del Sistema','Administrador Del Sistema'),
        ('Gerente','Gerente')
    )

    identification = models.CharField(max_length=40,blank=False,null=False,default='',verbose_name='Identificación')
    address = models.CharField(max_length=255,blank=True,null=True,verbose_name='Dirección')
    position = models.CharField(max_length=100,choices=POSITIONS,blank=True,null=True,verbose_name='Rol')
    phone = models.CharField(max_length=40,blank=True,null=True,verbose_name='Telefono')
    mobile = models.CharField(max_length=40,blank=True,null=True,verbose_name='Celular')
    

    def __str__(self):
        return self.email

    @property
    def get_absolute_detail_url(self):
        from django.urls import reverse_lazy
        return reverse_lazy('core:detail', args=[str(self.id)])

    @property
    def get_absolute_edit_url(self):
        from django.urls import reverse_lazy
        return reverse_lazy('core:update', args=[str(self.id)])

    @property
    def get_absolute_delete_url(self):
        from django.urls import reverse_lazy
        return reverse_lazy('core:delete', args=[str(self.id)])

User._meta.get_field('username').verbose_name = 'Nombre De Usuario'
User._meta.get_field('email').verbose_name = 'Correo Electronico'