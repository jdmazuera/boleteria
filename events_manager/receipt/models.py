from events_manager.core.models import BaseModel,User
from events_manager.core.validators import validator_greater_zero
from django.db import models

class Receipt(BaseModel):
    detail_view_name = 'receipt:detail_receipt'
    edit_view_name = 'receipt:update_receipt'
    delete_view_name = 'receipt:delete_receipt'

    salesman = models.ForeignKey(to=User,related_name='user_creator',on_delete=models.CASCADE,verbose_name='Vendedor')
    total = models.FloatField(default=0,blank=False,null=False,verbose_name='Total',validators=[validator_greater_zero])
    subtotal = models.FloatField(default=0,blank=False,null=False,verbose_name='Subtotal',validators=[validator_greater_zero])
    tax = models.FloatField(default=0,blank=False,null=False,verbose_name='Impuesto',validators=[validator_greater_zero])

    class Meta:
        permissions = [
            ("view_own_receipt", "Can View Only Own Receipts")
        ]
