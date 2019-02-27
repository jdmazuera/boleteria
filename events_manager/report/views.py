from django.shortcuts import render
from json import dumps,loads
from django.contrib.auth.decorators import login_required,permission_required
from django.http import HttpResponse
from events_manager.core.models import User
from events_manager.event.models import Event
from events_manager.ticket.models import Ticket
from django.db.models import Value, Q, Sum, Count
from django.db.models.functions import Concat

@login_required
@permission_required('core.view_report',raise_exception=False)
def sell_by_event(request):

    if request.is_ajax():
        body_unicode = request.body.decode('utf-8')
        body = loads(body_unicode)

        condiciones = {}

        if body.get('comprador'):
            condiciones['propietario__pk']=body['comprador'][0]
        if body.get('evento'):
            condiciones['event__pk']=body['evento'][0]
        if body.get('fecha_inicial'):
            condiciones['fecha_compra__gte']=body['fecha_inicial']
        if body.get('fecha_final'):
            condiciones['fecha_compra__lte']=body['fecha_final']
            
        tickets = Ticket.objects.filter(**condiciones).values('event__name').annotate(tickets_vendidos=Count('pk'))

        grafico = {
            'labels' : [],
            'data' : []
        }

        for ticket in tickets:
            grafico['labels'].append(ticket['event__name'])
            grafico['data'].append(ticket['tickets_vendidos'])

        return HttpResponse(dumps(grafico))

    users_list = User.objects.all().annotate(full_name=Concat('first_name',Value(' '),'last_name')).values_list('pk','full_name')
    events_list = Event.objects.all().values_list('pk','name')

    return render(
        request,
        'report/report_sell_by_event.html',
        {
            'initial_params':dumps({
                'users_list' : list(users_list),
                'events_list' : list(events_list)
            })
        }
    )