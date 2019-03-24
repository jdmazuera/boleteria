from django.db import models
from events_manager.core.models import BaseModel
from events_manager.type_event.models import TypeEvent

class Locality(BaseModel):
    detail_view_name = 'locality:detail'
    edit_view_name = 'locality:update'
    delete_view_name = 'locality:delete'
    name = models.CharField(max_length=250,blank=False,null=False,verbose_name='Nombre',unique=True)
    description = models.TextField(blank=True,null=True,verbose_name='Descripcion')
    event_type = models.ForeignKey(to=TypeEvent,on_delete=models.CASCADE,verbose_name='Tipo De Evento',related_name='event_type_locality',null=True,blank=False)

    def __str__(self):
        return self.name