from django.db import models
from django.utils.timezone import now
from events_manager.core.models import BaseModel
from events_manager.type_event.models import TypeEvent

class Event(BaseModel):
    detail_view_name = 'event:detail'
    edit_view_name = 'event:update'
    delete_view_name = 'event:delete'

    name = models.CharField(max_length=250,blank=False,null=False,verbose_name='Nombre')
    descripcion = models.TextField(blank=True,null=True,verbose_name='Descripcion')
    event_type = models.ForeignKey(to=TypeEvent,on_delete=models.CASCADE,verbose_name='Tipo De Evento',related_name='event_type_event',null=True,blank=False)
    date = models.DateTimeField(blank=False,null=False,default=now,verbose_name='Fecha Evento Y Hora Evento')
    ready_for_sale = models.BooleanField(default=False,verbose_name='Listo Para Vender')
    image_card = models.ImageField(upload_to = 'event_images/', default = 'event_images/default_image.png',verbose_name='Imagen Evento')

    def __str__(self):
        return self.name


    