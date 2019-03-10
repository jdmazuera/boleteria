from django.db import models
from django.utils.timezone import now
from events_manager.core.models import BaseModel
from django.core.exceptions import ValidationError

def validator_greater_zero(value):
    if value < 0:
        raise ValidationError(
            'El Valor Debe Ser Mayor A 0'
        )


class TypeEvent(BaseModel):
    name = models.CharField(max_length=250,blank=False,null=False,verbose_name='Nombre')
    description = models.TextField(blank=True,null=True,verbose_name='Descripcion')

    def __str__(self):
        return self.name

class Locality(BaseModel):
    name = models.CharField(max_length=250,blank=False,null=False,verbose_name='Nombre')
    description = models.TextField(blank=True,null=True,verbose_name='Descripcion')

class Event(BaseModel):
    self.detail_view_name = 'event:detail'
    self.edit_view_name = 'event:update'
    self.delete_view_name = 'event:delete'

    name = models.CharField(max_length=250,blank=False,null=False,verbose_name='Nombre')
    descripcion = models.TextField(blank=True,null=True,verbose_name='Descripcion')
    event_type = models.ForeignKey(to=TypeEvent,on_delete=models.CASCADE,blank=False,null=True,verbose_name='Tipo De Evento',related_name='event_type')
    date = models.DateField(blank=False,null=False,default=now,verbose_name='Fecha Evento')

    def __str__(self):
        return self.name

class EventLocality(BaseModel):
    event = models.ForeignKey(to=Event,on_delete=models.CASCADE,blank=False,null=True,verbose_name='Evento',related_name='event')
    locality = models.ForeignKey(to=Event,on_delete=models.CASCADE,blank=False,null=True,verbose_name='Localidad',related_name='locality')
    capacity = models.IntegerField(blank=False,null=False,default=0,verbose_name='Capacidad',validators=[validator_greater_zero])
    price = models.FloatField(blank=False,null=False,default=0,verbose_name='Capacidad',validators=[validator_greater_zero])


    