from events_manager.core.models import BaseModel,User
from events_manager.core.validators import validator_greater_zero
from django.db import models
from django.db.models import Sum
from django.forms import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from json import dumps
from django.conf import settings

class Receipt(BaseModel):
    detail_view_name = 'receipt:detail_receipt'
    edit_view_name = 'receipt:update_receipt'
    delete_view_name = 'receipt:delete_receipt'

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

    def to_json(self):
        receipt_dict = model_to_dict(self)

        items_dict = []

        for item in self.receipt.filter(is_active=True).order_by('id'):
            print(item.id)
            item_dict = model_to_dict(item)
            item_dict['event_name'] = item.event_locality.event.name
            item_dict['locality_name'] = item.event_locality.locality.name
            items_dict.append(item_dict)

        receipt_dict['items'] = items_dict
        receipt_dict['tax_percentage'] = settings.TAX_PERCENTAGE
        receipt_json = dumps(receipt_dict,cls=DjangoJSONEncoder)

        return receipt_json

    def sell(self,*args,**kwargs):
        self.confirmed = True
        super().save(*args, **kwargs)
        return True

    class Meta:
        permissions = [
            ("view_own_receipt", "Can View Only Own Receipts")
        ]
