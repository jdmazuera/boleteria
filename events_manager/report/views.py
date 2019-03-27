from django.shortcuts import render
from json import dumps,loads
from django.contrib.auth.decorators import login_required,permission_required
from django.http import HttpResponse
from events_manager.core.models import User
from events_manager.event.models import Event
from events_manager.ticket.models import Ticket
from events_manager.event_locality.models import EventLocality
from django.db.models import Value, Q, Sum, Count, F, FloatField
from django.db.models.functions import Concat, Cast

@login_required
@permission_required('core.view_report',raise_exception=False)
def sell_by_event(request):

    if request.is_ajax():
        body_unicode = request.body.decode('utf-8')
        body = loads(body_unicode)

        condiciones = {}

        if body.get('comprador'):
            condiciones['receipt__costumer__id']=body['comprador'][0]
        if body.get('evento'):
            condiciones['event_locality__event__id']=body['evento'][0]
        if body.get('fecha_inicial'):
            condiciones['creation_date__gte']=body['fecha_inicial']
        if body.get('fecha_final'):
            condiciones['creation_date__lte']=body['fecha_final']
            
        tickets = Ticket.objects.filter(**condiciones).values('event_locality__event__name').annotate(tickets_vendidos=Sum('quantity'))

        grafico = {
            'labels' : [],
            'data' : []
        }

        for ticket in tickets:
            grafico['labels'].append(ticket['event_locality__event__name'])
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

@login_required
@permission_required('core.view_report',raise_exception=False)
def top_costumers(request):

    if request.is_ajax():
        body_unicode = request.body.decode('utf-8')
        body = loads(body_unicode)

        condiciones = {}

        if body.get('evento'):
            condiciones['event_locality__event__id']=body['evento'][0]
        if body.get('fecha_inicial'):
            condiciones['creation_date__gte']=body['fecha_inicial']
        if body.get('fecha_final'):
            condiciones['creation_date__lte']=body['fecha_final']
        
        tickets = Ticket.objects.filter(**condiciones).annotate(costumer=Concat('receipt__costumer__first_name',Value(' '),'receipt__costumer__last_name')).values('costumer').annotate(ventas=Sum('subtotal'))

        grafico = {
            'labels' : [],
            'data' : []
        }

        for ticket in tickets:
            grafico['labels'].append(ticket['costumer'])
            grafico['data'].append(ticket['ventas'])

        return HttpResponse(dumps(grafico))

    users_list = User.objects.all().annotate(full_name=Concat('first_name',Value(' '),'last_name')).values_list('pk','full_name')
    events_list = Event.objects.all().values_list('pk','name')

    return render(
        request,
        'report/report_top_costumers.html',
        {
            'initial_params':dumps({
                'users_list' : list(users_list),
                'events_list' : list(events_list)
            })
        }
    )

@login_required
@permission_required('core.view_report',raise_exception=False)
def summerize_event_locality(request):

    if request.is_ajax():
        body_unicode = request.body.decode('utf-8')
        body = loads(body_unicode)

        condiciones = {}

        if body.get('evento'):
            condiciones['event__id']=body['evento'][0]
        if body.get('fecha_inicial'):
            condiciones['creation_date__gte']=body['fecha_inicial']
        if body.get('fecha_final'):
            condiciones['creation_date__lte']=body['fecha_final']
        
        summerize = list(EventLocality.objects.filter(**condiciones).annotate(
                sold_float=Cast('sold', FloatField()),
                capacity_float=Cast('capacity', FloatField())
        ).annotate(
            percentage_occupation=F('sold_float')/F('capacity_float')*100
        ).values('event__name','locality__name','capacity','availability','sold','percentage_occupation'))

        return HttpResponse(dumps(summerize))

    users_list = User.objects.all().annotate(full_name=Concat('first_name',Value(' '),'last_name')).values_list('pk','full_name')
    events_list = Event.objects.all().values_list('pk','name')

    return render(
        request,
        'report/report_summarize_event_locality.html',
        {
            'initial_params':dumps({
                'users_list' : list(users_list),
                'events_list' : list(events_list)
            })
        }
    )


@login_required
@permission_required('core.view_report',raise_exception=False)
def pareto_costumers(request):

    if request.is_ajax():
        body_unicode = request.body.decode('utf-8')
        body = loads(body_unicode)

        condiciones = {}

        if body.get('evento'):
            condiciones['event_locality__event__id']=body['evento'][0]
        if body.get('fecha_inicial'):
            condiciones['creation_date__gte']=body['fecha_inicial']
        if body.get('fecha_final'):
            condiciones['creation_date__lte']=body['fecha_final']
            
        total_sold = Ticket.objects.filter(**condiciones).aggregate(ventas=Sum('subtotal')).get('ventas',0) * 0.80
        costumers = Ticket.objects.filter(**condiciones).values('receipt__costumer__first_name','receipt__costumer__last_name').annotate(ventas=Sum('subtotal')).order_by('-ventas')

        running_total = 0
        pareto_costumers_label = []
        pareto_costumers_data = []

        for item in costumers:
            running_total += item.get('ventas',0)

            if not pareto_costumers_data or running_total <= total_sold:
                pareto_costumers_label.append((item['receipt__costumer__first_name']+' '+item['receipt__costumer__last_name']))
                pareto_costumers_data.append(item['ventas'])            

        chart_data = {
            'labels' : pareto_costumers_label,
            'datasets' : [
                {
                    'label': 'Comprado',
                    'stack': 'Stack 0',
                    'data': pareto_costumers_data
                }
            ]
        }

        return HttpResponse(dumps(chart_data))

    users_list = User.objects.all().annotate(full_name=Concat('first_name',Value(' '),'last_name')).values_list('pk','full_name')
    events_list = Event.objects.all().values_list('pk','name')

    return render(
        request,
        'report/report_pareto_costumers.html',
        {
            'initial_params':dumps({
                'users_list' : list(users_list),
                'events_list' : list(events_list)
            })
        }
    )