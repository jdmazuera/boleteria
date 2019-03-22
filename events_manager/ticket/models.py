from django.db import models
from events_manager.event_locality.models import EventLocality
from events_manager.core.models import User,BaseModel
from events_manager.receipt.models import Receipt
from django.utils.timezone import now
from events_manager.core.validators import validator_greater_zero
from django.conf import settings

class Ticket(BaseModel):
    detail_view_name = 'ticket:detail'
    edit_view_name = 'ticket:update'
    delete_view_name = 'ticket:delete'

    error_messages = {
        'blank' : 'El Campo No Puede Estar En Blanco',
        'invalid' : 'El Valor No Es Valido',
        'invalid_choice' : 'Opcion No Valida',
        'unique' : 'El Ticket Debe Ser Unico'
    }

    event_locality = models.ForeignKey(to=EventLocality,on_delete=models.CASCADE,related_name='event_locality',verbose_name='Localidad Evento',error_messages=error_messages,null=True,blank=False)
    receipt = models.ForeignKey(to=Receipt,on_delete=models.CASCADE,related_name='receipt',verbose_name='Factura',error_messages=error_messages,null=True,blank=False)
    price = models.FloatField(default=0,blank=False,null=False,verbose_name='Precio',validators=[validator_greater_zero])
    tax = models.FloatField(default=0,blank=False,null=False,verbose_name='Impuesto',validators=[validator_greater_zero])
    quantity = models.IntegerField(default=0,blank=False,null=False,verbose_name='Cantidad',validators=[validator_greater_zero])
    subtotal = models.FloatField(default=0,blank=False,null=False,verbose_name='Subtotal',validators=[validator_greater_zero])
    total = models.FloatField(default=0,blank=False,null=False,verbose_name='Total',validators=[validator_greater_zero])

    def save(self,*args, **kwargs):
        self.subtotal = self.price * self.quantity
        self.tax = self.subtotal * settings.TAX_PERCENTAGE
        self.total = self.subtotal + self.tax
        super().save(*args, **kwargs)

    class Meta:
        permissions = [
            ("view_own_ticket", "Can View Only Own Tickets")
        ]