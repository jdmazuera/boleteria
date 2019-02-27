from django.db import models
from events_manager.event.models import Event
from events_manager.core.models import User
from django.utils.timezone import now
from django.urls import reverse

class Ticket(models.Model):
    ESTADOS = (
        ('Activa','Activa'),
        ('Anulada','Anulada')
    )

    error_messages = {
        'blank' : 'El Campo No Puede Estar En Blanco',
        'invalid' : 'El Valor No Es Valido',
        'invalid_choice' : 'Opcion No Valida',
        'unique' : 'El Ticket Debe Ser Unico'
    }
    METODOS_PAGO = (
        ('Efectivo','Efectivo'),
        ('Tarjeta Debido','Tarjeta Debido'),
        ('Credito','Credito')
    )

    price = models.FloatField(blank=False,null=False,verbose_name='Precio',error_messages=error_messages)
    estado = models.CharField(max_length=250,blank=False,null=False,verbose_name='Estado',choices=ESTADOS,default='Activa',error_messages=error_messages)
    event = models.ForeignKey(Event, on_delete=models.CASCADE,related_name='event_ticket',verbose_name='Evento',error_messages=error_messages)
    date = models.DateField(default=now,blank=False,null=False,verbose_name='Fecha',error_messages=error_messages)
    propietario = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=True,related_name='propietario',error_messages=error_messages)
    is_active = models.BooleanField(default=True,verbose_name='Activo')
    metodo_pago = models.CharField(max_length=250,blank=False,null=False,verbose_name='Metodo De Pago',choices=METODOS_PAGO,default='Efectivo',error_messages=error_messages)
    iva = models.FloatField(blank=True,null=True,verbose_name='IVA')
    subtotal = models.FloatField(blank=True,null=True,verbose_name='Subtotal')
    fecha_compra = models.DateField(default=now,blank=False,null=False,verbose_name='Fecha Compra',error_messages=error_messages)

    def save(self,*args, **kwargs):
        self.iva = self.price * 0.19
        self.subtotal = self.price * 0.81
        super(Ticket, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ticket:detail', kwargs={'pk': self.pk})

    @property
    def get_absolute_detail_url(self):
        from django.urls import reverse_lazy
        return reverse_lazy('ticket:detail', args=[str(self.id)])

    @property
    def get_absolute_edit_url(self):
        from django.urls import reverse_lazy
        return reverse_lazy('ticket:update', args=[str(self.id)])

    @property
    def get_absolute_delete_url(self):
        from django.urls import reverse_lazy
        return reverse_lazy('ticket:delete', args=[str(self.id)])

    def delete(self,*args, **kwargs):
        self.is_active = False
        self.save()

    def __str__(self):
        return '%s - Boleto %s' % (self.event.name, self.pk)

    class Meta:
        permissions = [
            ("view_own_ticket", "Can View Only Own Tickets")
        ]