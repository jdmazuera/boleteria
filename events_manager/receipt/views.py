from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from json import dumps,loads
from django.contrib.auth.decorators import login_required,permission_required
from django.http import HttpResponse,HttpResponseRedirect

from events_manager.core.models import User
from events_manager.event.models import Event
from events_manager.event_locality.models import EventLocality
from events_manager.locality.models import Locality
from events_manager.receipt.models import Receipt
from events_manager.ticket.models import Ticket
from events_manager.type_event.models import TypeEvent

from django.db.models import Value, Q, Sum, Count
from django.db.models.functions import Concat
from django.views.generic import View,DetailView,ListView,CreateView,DeleteView,UpdateView
from django.utils.decorators import method_decorator
from json import loads,dumps
from django.core.exceptions import ObjectDoesNotExist
from events_manager.receipt.forms import ReceiptForm
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

            if ticket.receipt.get_items().count() <= 0:
                ticket.receipt.true_delete()
                request.session['shopping_car'] = None
                return redirect('receipt:detail_shopping_car')

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

        users = User.objects.filter(is_active=True).annotate(full_name=Concat('first_name',Value(' '),'last_name')).values_list('id','full_name')

        return render(
            request,
            'receipt/shopping_car_detail.html',
            {
                'receipt' : receipt.to_json(),
                'pay_method_list': dumps(Receipt.PAY_METHODS),
                'costumer_list': dumps(list(users))
            }
        )

    def post(self,request,*args,**kwargs):
        try:
            values = request.POST.dict()
            shopping_car = loads(request.session['shopping_car'])
            receipt = Receipt.objects.get(id=shopping_car['receipt_session_id'])

            if receipt.get_items().count() <= 0:
                return redirect('receipt:detail_shopping_car')


            receipt.pay_method = eval(values['pay_method'])[0]

            

            if request.user.has_perm('receipt.sell'):
                id_costumer = eval(values['costumer'])[0]
                costumer = User.objects.get(id=id_costumer)
                receipt.costumer = costumer
                receipt.salesman = request.user
            else:
                receipt.costumer = request.user

            no_avaliable = receipt.sell()

            if no_avaliable:
                return render(
                    request,
                    'receipt/shopping_car_detail.html',
                    {
                        'receipt' : receipt.to_json(),
                        'pay_method_list': dumps(Receipt.PAY_METHODS),
                        'no_avaliable' : no_avaliable
                    }
                )

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
        except:
            return redirect('receipt:detail_shopping_car')


        return HttpResponseRedirect(reverse_lazy('receipt:detail',args=[receipt.id]))

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('receipt.view_receipt',raise_exception=False), name='dispatch')
class DetailReceiptView(DetailView):
    model = Receipt

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('receipt.view_receipt',raise_exception=False), name='dispatch')
class ReceiptListView(ListView):
    model = Receipt

    def post(self,request):
        keyword = request.POST.get('keyword')

        receipts = self.get_queryset()

        receipts = receipts.filter(
            Q(identifier__icontains=keyword)
            |Q(costumer__first_name__icontains=keyword)
            |Q(costumer__last_name__icontains=keyword)
            |Q(costumer__identification__icontains=keyword)
            |Q(salesman__first_name__icontains=keyword)
            |Q(salesman__last_name__icontains=keyword)
            |Q(salesman__identification__icontains=keyword)
            |Q(pay_method__icontains=keyword)
        )

        return render(
            request,
            'receipt/receipt_list.html',
            {
                'object_list': receipts,
                'keyword' : keyword
            }
        )

    def get_queryset(self):
        if self.request.user.has_perm('receipt.view_all_receipts'):
            receipts = Receipt.objects.filter(confirmed=True)
        else:
            receipts = Receipt.objects.filter(costumer=self.request.user,confirmed=True)
        return receipts

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('receipt.add_receipt',raise_exception=False), name='dispatch')
class ReceiptCreateView(CreateView):
    model = Receipt
    success_url = reverse_lazy('receipt:list')
    form_class = ReceiptForm

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('receipt.change_receipt',raise_exception=False), name='dispatch')
class ReceiptUpdateView(UpdateView):
    model = Receipt
    success_url = reverse_lazy('receipt:list')
    form_class = ReceiptForm

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('receipt.delete_receipt',raise_exception=False), name='dispatch')
class ReceiptDeleteView(DeleteView):
    model = Receipt
    success_url = reverse_lazy('receipt:list')
    fields = ['name']
    




