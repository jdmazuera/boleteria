from django.db import models
from events_manager.event.models import Event

class Ticket(models.Model):
    name = models.CharField(max_length=250,blank=False,null=False,verbose_name='Nombre')
    price = models.FloatField(blank=False,null=False,verbose_name='Precio')
    event = models.ForeignKey(Event, on_delete=models.CASCADE,related_name='event_ticket')
    date = models.DateField(blank=False,null=False,verbose_name='Fecha')
