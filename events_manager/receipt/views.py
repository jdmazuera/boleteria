from django.shortcuts import render
from json import dumps,loads
from django.contrib.auth.decorators import login_required,permission_required
from django.http import HttpResponse
from events_manager.core.models import User
from events_manager.event.models import Event
from events_manager.ticket.models import Ticket
from events_manager.event_locality.models import EventLocality
from events_manager.locality.models import Locality
from django.db.models import Value, Q, Sum, Count
from django.db.models.functions import Concat
from django.views.generic import View
from django.utils.decorators import method_decorator
from json import loads,dumps
from django.core.exceptions import ObjectDoesNotExist
    

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('receipt.buy',raise_exception=False), name='dispatch')
class AddToShoppingCarView(View):
    def post(self,request, *args, **kwargs):
        if request.is_ajax():
            body_unicode = request.body.decode('utf-8')
            item = loads(body_unicode)

            try:
                shopping_car = loads(request.session['shopping_car'])
            except:
                shopping_car = [[],[]]
            
            if item in shopping_car[0]:
                index = shopping_car[0].index(item)
                shopping_car[1][index] += 1
            else:
                shopping_car[0].append(item)
                shopping_car[1].append(1)

            request.session['shopping_car'] = dumps(shopping_car)

            return HttpResponse(request.session['shopping_car'])

        return HttpResponse('fail')


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('receipt.buy',raise_exception=False), name='dispatch')
class DetailShoppingCar(View):
    def get(self,request,*args,**kwargs):

        if request.session.get('shopping_car'):
            shopping_car = loads(request.session.get('shopping_car'))
        else:
            shopping_car = [[],[]]

        shopping_car_detailed = []

        for index,item in enumerate(shopping_car[0]):
            try:
                event_locality = EventLocality.objects.get(pk=item)
                shopping_car_detailed.append(
                    {
                        'event_locality_id':event_locality.id,
                        'event_name':event_locality.event.name,
                        'locality_name':event_locality.locality.name,
                        'price':event_locality.price,
                        'quantity':shopping_car[1][index]
                    }
                )
            except ObjectDoesNotExist:
                pass


        return render(
            request,
            'receipt/shopping_car_detail.html',
            {
                'shopping_car_detail' : dumps(shopping_car_detailed)
            }
        )





