from django.db import models
from events_manager.core.models import BaseModel
from events_manager.core.validators import validator_greater_zero
from events_manager.event.models import Event
from events_manager.locality.models import Locality

class EventLocality(BaseModel):
    detail_view_name = 'event_locality:detail'
    edit_view_name = 'event_locality:update'
    delete_view_name = 'event_locality:delete'
    event = models.ForeignKey(to=Event,on_delete=models.CASCADE,verbose_name='Evento',related_name='event',null=True,blank=False)
    locality = models.ForeignKey(to=Locality,on_delete=models.CASCADE,verbose_name='Localidad',related_name='locality',null=True,blank=False)
    capacity = models.IntegerField(blank=False,null=False,default=0,verbose_name='Capacidad',validators=[validator_greater_zero])
    availability = models.IntegerField(blank=False,null=False,default=0,verbose_name='Disponibilidad')
    price = models.FloatField(blank=False,null=False,default=0,verbose_name='Capacidad',validators=[validator_greater_zero])

    def save(self,*args,**kwargs):
        if not self.id:
            self.availability = self.capacity
        super().save(*args,**kwargs)

    def __str__(self):
        return self.event.name + ' - ' + self.locality.name

    def to_discount(self,quantity,commit=False):
        if self.availability >= quantity and quantity >= 0:
            self.availability -= quantity
            if commit:
                self.save()
            return True
        else:
            return False
        