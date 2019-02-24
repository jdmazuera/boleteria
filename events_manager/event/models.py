from django.db import models
from django.utils.timezone import now

# Create your models here.
class Event(models.Model):

    TYPES = (
        ('Futbol','Futbol'),
        ('Tenis ','Tenis '),
        ('Béisbol','Béisbol')
    )

    DIVISIONS = (
        ('Primera','Primera'),
        ('Segunda ','Segunda '),
        ('Tercera','Tercera')
    )

    name = models.CharField(max_length=250,blank=False,null=False,verbose_name='Nombre')
    descripcion = models.TextField(blank=True,null=True,verbose_name='Descripcion')
    event_type = models.CharField(max_length=250,blank=False,null=False,verbose_name='Tipo',choices=TYPES)
    capacity = models.IntegerField(blank=False,null=False,default=0,verbose_name='Capacidad')
    date = models.DateField(blank=False,null=False,default=now,verbose_name='Fecha')
    cupos_restantes = models.IntegerField(blank=False,null=False,default=0,verbose_name='Cupos Restantes')
    division = models.CharField(max_length=250,blank=False,null=True,verbose_name='Division',choices=DIVISIONS)
    equipo_local = models.CharField(max_length=250,blank=False,null=True,verbose_name='Equipo Local')
    equipo_visitante = models.CharField(max_length=250,blank=False,null=True,verbose_name='Equipo Visitante')
    is_active = models.BooleanField(default=True,verbose_name='Activo')

    @property
    def get_absolute_detail_url(self):
        from django.urls import reverse_lazy
        return reverse_lazy('event:detail', args=[str(self.id)])

    @property
    def get_absolute_edit_url(self):
        from django.urls import reverse_lazy
        return reverse_lazy('event:update', args=[str(self.id)])

    @property
    def get_absolute_delete_url(self):
        from django.urls import reverse_lazy
        return reverse_lazy('event:delete', args=[str(self.id)])

    def save(self,*args, **kwargs):
        if not self.pk:
            self.cupos_restantes = self.capacity
        super(Event, self).save(*args, **kwargs)

    def delete(self,*args, **kwargs):
        self.is_active = False
        self.save()