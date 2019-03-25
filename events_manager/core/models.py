from django.db import models
from django.contrib.auth.models import AbstractUser,Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
from django_currentuser.db.models import CurrentUserField

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
                content_type__model__in=('event','ticket','user','locality','event_locality','receipt')
            )
            self.user_permissions.set(permissions)

        elif self.position == 'Vendedor':
            permissions = Permission.objects.filter(
                content_type__model__in=('ticket','user','receipt','event')
            ).exclude(
                codename__in=(
                    'view_report',
                    'add_receipt',
                    'change_receipt',
                    'delete_receipt',
                    'add_ticket',
                    'delete_ticket',
                    'add_event',
                    'change_event',
                    'delete_event'
                )
            )
            self.user_permissions.set(permissions)

        elif self.position == 'Cliente':
            permissions = Permission.objects.filter(codename__in=('view_event','view_ticket','add_ticket','view_user','buy'))
            self.user_permissions.set(permissions)

        else:
            self.position = 'Cliente'
            permissions = Permission.objects.filter(codename__in=('user_view','view_event','view_ticket','view_user','buy'))
            self.user_permissions.set(permissions)

        super(User, self).save(*args, **kwargs)

    def delete(self,*args, **kwargs):
        self.is_active = False
        self.save()

    def __str__(self):
        return self.get_full_name()
    
    class Meta:
        permissions = [
            ("view_report", "Can View Report Module"),
            ("view_all_user", "Can View All Users")
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
User._meta.get_field('first_name').blank = False
User._meta.get_field('last_name').verbose_name = 'Apellido'
User._meta.get_field('last_name').blank = False
User._meta.get_field('is_active').verbose_name = 'Activo'
User._meta.get_field('is_active').help_text = 'Desactiva el acceso al usuario a las caracteristicas del sistema'

class BaseManager(models.Manager):
    def get_queryset(self):
        return super(BaseManager, self).get_queryset().filter(is_active=True)

class BaseModel(models.Model):
    detail_view_name = None
    edit_view_name = None
    delete_view_name = None

    objects = BaseManager()

    user_creator = CurrentUserField(verbose_name='Usuario Creador')
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

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        abstract = True