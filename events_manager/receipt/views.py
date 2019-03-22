from django.shortcuts import render
from django.urls import reverse_lazy
from json import dumps,loads
from django.contrib.auth.decorators import login_required,permission_required
from django.http import HttpResponse,HttpResponseRedirect
from events_manager.core.models import User
from events_manager.event.models import Event
from events_manager.ticket.models import Ticket
from events_manager.event_locality.models import EventLocality
from events_manager.receipt.models import Receipt
from events_manager.ticket.models import Ticket
from events_manager.locality.models import Locality
from django.db.models import Value, Q, Sum, Count
from django.db.models.functions import Concat
from django.views.generic import View,DetailView
from django.utils.decorators import method_decorator
from json import loads,dumps
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
    

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('receipt.buy',raise_exception=False), name='dispatch')
class AddToShoppingCarView(View):
    def post(self,request, *args, **kwargs):
        if request.is_ajax():
            body_unicode = request.body.decode('utf-8')
            item = loads(body_unicode)

            try:
                event_locality = EventLocality.objects.get(id=item,is_active=True)
            except ObjectDoesNotExist:
                return HttpResponse('Event Locality doesn\'t exists')

            try:
                shopping_car = loads(request.session['shopping_car'])
            except:
                shopping_car = {
                    'receipt_session_id' : None,
                    'receipt_items_quantity' : None
                }
            
            try:
                receipt = Receipt.objects.get(id=shopping_car['receipt_session_id'],is_active=True)
            except:
                receipt = Receipt()
                if not request.user.position == 'Vendedor':
                    receipt.salesman = request.user
                receipt.save()
                receipt.identifier = 'FV - '+str(receipt.id * 1000) + '-' + str((receipt.id * 1000)%95)
                receipt.save()

            try:
                ticket = Ticket.objects.get(receipt=receipt,event_locality=event_locality,is_active=True)
                ticket.quantity += 1
                ticket.save()
            except ObjectDoesNotExist:
                ticket = Ticket()
                ticket.receipt = receipt
                ticket.event_locality = event_locality
                ticket.price = event_locality.price
                ticket.quantity = 1
                ticket.save()

            shopping_car['receipt_session_id'] = receipt.id
            shopping_car['receipt_items_quantity'] = receipt.quantity

            request.session['shopping_car'] = dumps(shopping_car)

            return HttpResponse(request.session['shopping_car'])

        return HttpResponse('fail')

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('receipt.buy',raise_exception=False), name='dispatch')
class DeleteItemShoppingCarView(View):
    def post(self,request, *args, **kwargs):
        if request.is_ajax():
            params = loads(request.body.decode('utf-8'))
            ticket = Ticket.objects.get(id=params['id'])
            ticket.delete()

            shopping_car = loads(request.session['shopping_car'])
            shopping_car['receipt_items_quantity'] = ticket.receipt.quantity
            request.session['shopping_car'] = dumps(shopping_car)

            return HttpResponse(ticket.receipt.to_json())

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('receipt.buy',raise_exception=False), name='dispatch')
class UpdateItemShoppingCarView(View):
    def post(self,request, *args, **kwargs):
        if request.is_ajax():
            params = loads(request.body.decode('utf-8'))
            ticket = Ticket.objects.get(id=params['id'],is_active=True)
            ticket.quantity = params['quantity']
            ticket.save()

            shopping_car = loads(request.session['shopping_car'])
            shopping_car['receipt_items_quantity'] = ticket.receipt.quantity
            request.session['shopping_car'] = dumps(shopping_car)

            return HttpResponse('success')

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('receipt.buy',raise_exception=False), name='dispatch')
class DetailShoppingCar(View):
    def get(self,request,*args,**kwargs):
        if request.session.get('shopping_car'):
            shopping_car = loads(request.session.get('shopping_car'))
        else:
            shopping_car = {}

        try:
            receipt = Receipt.objects.get(id=shopping_car.get('receipt_session_id'))
        except ObjectDoesNotExist:
            return render(
                request,
                'receipt/shopping_car_detail.html',
                {
                    'pay_method_list': dumps(Receipt.PAY_METHODS),
                    'shopping_car_empty': True
                }
            )

        return render(
            request,
            'receipt/shopping_car_detail.html',
            {
                'receipt' : receipt.to_json(),
                'pay_method_list': dumps(Receipt.PAY_METHODS)
            }
        )

    def post(self,request,*args,**kwargs):
        values = request.POST.dict()

        shopping_car = loads(request.session['shopping_car'])

        

        try:
            receipt = Receipt.objects.get(id=shopping_car['receipt_session_id'])
            receipt.pay_method = eval(values['pay_method'])[0]
            receipt.sell()
            request.session['shopping_car'] = None
        except ObjectDoesNotExist:
            return render(
                request,
                'receipt/shopping_car_detail.html',
                {
                    'receipt' : receipt.to_json(),
                    'pay_method_list': dumps(Receipt.PAY_METHODS)
                }
            )

        return HttpResponseRedirect(reverse_lazy('receipt:detail',args=[receipt.id]))

class DetailReceiptView(DetailView):
    model = Receipt
    




