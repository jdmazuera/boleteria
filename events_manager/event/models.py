from django.db import models

# Create your models here.
class Event(models.Model):

    TYPES = (
        ('concierto','Concierto'),
        ('cultural','Cultural'),
        ('deportivo','Deportivo'),
        ('clerico','Clerico')
    )

    name = models.CharField(max_length=250,blank=False,null=False,verbose_name='Nombre')
    event_type = models.CharField(max_length=250,blank=False,null=False,verbose_name='Tipo',choices=TYPES)
    capacity = models.IntegerField(blank=False,null=False,verbose_name='Capacidad')
    date = models.DateField(blank=False,null=False,verbose_name='Fecha')