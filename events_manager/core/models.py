from django.db import models
from django.contrib.auth.models import AbstractUser,Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now

class User(AbstractUser):

    POSITIONS = (
        ('Gerente','Gerente'),
        ('Administrador Del Sistema','Administrador Del Sistema'),
        ('Vendedor','Vendedor'),
        ('Cliente','Cliente')
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

    def save(self,*args, **kwargs):
        super(User, self).save(*args, **kwargs)
        
        self.user_permissions.clear()

        if self.position == 'Administrador Del Sistema':
            permissions = Permission.objects.all()
            self.user_permissions.set(permissions)

        elif self.position == 'Gerente':
            permissions = Permission.objects.filter(
                content_type__model__in=('event','ticket','user')
            ).exclude(codename='view_own_ticket')
            self.user_permissions.set(permissions)

        elif self.position == 'Vendedor':
            permissions = Permission.objects.filter(
                content_type__model__in=('ticket','user')
            ).exclude(codename__in=('view_report','view_own_ticket'))
            self.user_permissions.set(permissions)

        elif self.position == 'Cliente':
            permissions = Permission.objects.filter(codename__in=('view_event','view_ticket','add_ticket','view_user','view_own_ticket'))
            self.user_permissions.set(permissions)

        else:
            self.position = 'Cliente'
            permissions = Permission.objects.filter(codename__in=('user_view','view_event','view_ticket','view_user','view_own_ticket'))
            self.user_permissions.set(permissions)

        super(User, self).save(*args, **kwargs)

    def delete(self,*args, **kwargs):
        self.is_active = False
        self.save()

    def __str__(self):
        return self.get_full_name()
    
    class Meta:
        permissions = [
            ("view_report", "Can View Report Module")
        ]

User._meta.get_field('username').verbose_name = 'Nombre De Usuario'
User._meta.get_field('username').help_text = 'Sin espacios ni caracteres especiales'
User._meta.get_field('username').error_messages = {
    'blank' : 'El Campo No Puede Estar En Blanco',
    'invalid' : 'El Valor No Es Valido',
    'invalid_choice' : 'Opcion No Valida',
    'unique' : 'El Usuario Debe Ser Unico'
}

User._meta.get_field('email').verbose_name = 'Correo Electronico'
User._meta.get_field('first_name').verbose_name = 'Nombre'
User._meta.get_field('last_name').verbose_name = 'Apellido'
User._meta.get_field('is_active').verbose_name = 'Activo'
User._meta.get_field('is_active').help_text = 'Desactiva el acceso al usuario a las caracteristicas del sistema'

class BaseModel(models.Model):
    detail_view_name = None
    edit_view_name = None
    delete_view_name = None


    user_creator = models.ForeignKey(to=User,on_delete=models.CASCADE,verbose_name='Usuario Creador',null=True,blank=False)
    is_active = models.BooleanField(default=True,verbose_name='Activo')
    creation_date = models.DateTimeField(default=now,verbose_name='Fecha De Creación',null=True,blank=False)

    @property
    def get_absolute_detail_url(self):
        from django.urls import reverse_lazy
        return reverse_lazy(self.detail_view_name, args=[str(self.id)])

    @property
    def get_absolute_edit_url(self):
        from django.urls import reverse_lazy
        return reverse_lazy(self.edit_view_name, args=[str(self.id)])

    @property
    def get_absolute_delete_url(self):
        from django.urls import reverse_lazy
        return reverse_lazy(self.delete_view_name, args=[str(self.id)])

    def delete(self,*args, **kwargs):
        self.is_active = False
        self.save()

    def true_delete(self,*args, **kwargs):
        super().delete()

    class Meta:
        abstract = True