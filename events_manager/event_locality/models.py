from django.db import models
from events_manager.core.models import BaseModel
from events_manager.core.validators import validator_greater_zero
from events_manager.event.models import Event
from events_manager.locality.models import Locality

class EventLocality(BaseModel):
    detail_view_name = 'eventlocality:detail'
    edit_view_name = 'eventlocality:update'
    delete_view_name = 'eventlocality:delete'
    event = models.ForeignKey(to=Event,on_delete=models.CASCADE,verbose_name='Evento',related_name='event',null=True,blank=False)
    locality = models.ForeignKey(to=Locality,on_delete=models.CASCADE,verbose_name='Localidad',related_name='locality',null=True,blank=False)
    capacity = models.IntegerField(blank=False,null=False,default=0,verbose_name='Capacidad',validators=[validator_greater_zero])
    availability = models.IntegerField(blank=False,null=False,default=0,verbose_name='Disponibilidad')
    price = models.FloatField(blank=False,null=False,default=0,verbose_name='Capacidad',validators=[validator_greater_zero])
    identifier = models.CharField(max_length=250,blank=True,null=True,verbose_name='Codigo')
    sold = models.IntegerField(blank=False,null=False,default=0,verbose_name='Vendidas')

    def save(self,*args,**kwargs):
        self.availability = int(self.capacity) - self.sold
        super().save(*args,**kwargs)
        self.identifier = 'Localidad Evento - ' + str(self.id * 10000) + ' - ' + str((self.id * 10000)%456)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.event.name + ' - ' + self.locality.name

    def to_discount(self,quantity,commit=False):
        if self.availability >= quantity and quantity >= 0:
            self.availability -= quantity
            self.sold += quantity
            if commit:
                self.save()
            return True
        else:
            return False
        