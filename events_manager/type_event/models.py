from django.db import models
from events_manager.core.models import BaseModel

class TypeEvent(BaseModel):
    detail_view_name = 'type_event:detail'
    edit_view_name = 'type_event:update'
    delete_view_name = 'type_event:delete'
    name = models.CharField(max_length=250,blank=False,null=False,verbose_name='Nombre',unique=True)
    description = models.TextField(blank=True,null=True,verbose_name='Descripcion')

    def __str__(self):
        return self.name
