from django.db import models
from django.utils.timezone import now
from events_manager.core.models import BaseModel
from events_manager.core.validators import validator_greater_zero


class TypeEvent(BaseModel):
    detail_view_name = 'event:detail_type_event'
    edit_view_name = 'event:update_type_event'
    delete_view_name = 'event:delete_type_event'
    name = models.CharField(max_length=250,blank=False,null=False,verbose_name='Nombre')
    description = models.TextField(blank=True,null=True,verbose_name='Descripcion')

    def __str__(self):
        return self.name

class Locality(BaseModel):
    detail_view_name = 'event:detail_locality'
    edit_view_name = 'event:update_locality'
    delete_view_name = 'event:delete_locality'
    name = models.CharField(max_length=250,blank=False,null=False,verbose_name='Nombre')
    description = models.TextField(blank=True,null=True,verbose_name='Descripcion')
    event_type = models.ForeignKey(to=TypeEvent,on_delete=models.CASCADE,verbose_name='Tipo De Evento',related_name='event_type_locality',null=True,blank=False)

class Event(BaseModel):
    detail_view_name = 'event:detail'
    edit_view_name = 'event:update'
    delete_view_name = 'event:delete'

    name = models.CharField(max_length=250,blank=False,null=False,verbose_name='Nombre')
    descripcion = models.TextField(blank=True,null=True,verbose_name='Descripcion')
    event_type = models.ForeignKey(to=TypeEvent,on_delete=models.CASCADE,verbose_name='Tipo De Evento',related_name='event_type_event',null=True,blank=False)
    date = models.DateField(blank=False,null=False,default=now,verbose_name='Fecha Evento')

    def __str__(self):
        return self.name

class EventLocality(BaseModel):
    event = models.ForeignKey(to=Event,on_delete=models.CASCADE,verbose_name='Evento',related_name='event',null=True,blank=False)
    locality = models.ForeignKey(to=Event,on_delete=models.CASCADE,verbose_name='Localidad',related_name='locality',null=True,blank=False)
    capacity = models.IntegerField(blank=False,null=False,default=0,verbose_name='Capacidad',validators=[validator_greater_zero])
    price = models.FloatField(blank=False,null=False,default=0,verbose_name='Capacidad',validators=[validator_greater_zero])


    