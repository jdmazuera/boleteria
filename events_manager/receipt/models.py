from events_manager.core.models import BaseModel,User
from events_manager.core.validators import validator_greater_zero
from django.db import models
from django.db.models import Sum
from django.forms import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from json import dumps
from django.conf import settings

class Receipt(BaseModel):
    detail_view_name = 'receipt:detail'
    edit_view_name = 'receipt:update'
    delete_view_name = 'receipt:delete'

    PAY_METHODS = (
        ('Efectivo','Efectivo'),
        ('Tarjeta Debito','Tarjeta Debito'),
        ('Tarjeta Credito','Tarjeta Credito')
    )

    identifier = models.CharField(max_length=100,blank=False,null=True,verbose_name="Consecutivo")
    salesman = models.ForeignKey(to=User,related_name='user_creator',on_delete=models.CASCADE,verbose_name='Vendedor',blank=True,null=True)
    pay_method = models.CharField(max_length=100,blank=False,null=True,verbose_name='Metodo De Pago',choices=PAY_METHODS)
    confirmed = models.BooleanField(default=False,blank=True,null=True,verbose_name='Venta Confirmada')
    costumer = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='receipts',verbose_name='Cliente',blank=True,null=True)

    @property
    def total(self):
        return self.receipt.filter(is_active=True).aggregate(Sum('total')).get('total__sum', 0.00)
    
    @property
    def tax(self):
        return self.receipt.filter(is_active=True).aggregate(Sum('tax')).get('tax__sum', 0.00)
    
    @property
    def subtotal(self):
        return self.receipt.filter(is_active=True).aggregate(Sum('subtotal')).get('subtotal__sum', 0.00)

    @property
    def quantity(self):
        return self.receipt.filter(is_active=True).aggregate(Sum('quantity')).get('quantity__sum', 0.00)
    
    def __str__(self):
        return self.identifier

    def get_items(self):
        return self.receipt.filter(is_active=True).order_by('id')

    def to_json(self):
        receipt_dict = model_to_dict(self)

        items_dict = []

        for item in self.receipt.filter(is_active=True).order_by('id'):
            item_dict = model_to_dict(item)
            item_dict['event_name'] = item.event_locality.event.name
            item_dict['locality_name'] = item.event_locality.locality.name
            items_dict.append(item_dict)

        receipt_dict['items'] = items_dict
        receipt_dict['tax_percentage'] = settings.TAX_PERCENTAGE
        receipt_json = dumps(receipt_dict,cls=DjangoJSONEncoder)

        return receipt_json

    def sell(self,*args,**kwargs):
        no_avaliable = []
        for item in self.receipt.filter(is_active=True):
            if not item.event_locality.to_discount(item.quantity):
                no_avaliable.append(item)

        if no_avaliable:
            return no_avaliable

        for item in self.receipt.filter(is_active=True):
            item.event_locality.to_discount(item.quantity,True)

        self.confirmed = True
        super().save(*args, **kwargs)

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        self.identifier = 'FV - '+str(self.id * 1000) + '-' + str((self.id * 1000)%95)
        super().save(*args,**kwargs)

    class Meta:
        permissions = [
            ("sell", "Can sell tickets to others users"),
            ("buy", "Can buy tickets"),
            ("view_all_receipts", "Can view all receipts")
        ]
