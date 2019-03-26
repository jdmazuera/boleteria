from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required,permission_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db.models import Q

from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from rest_framework.generics import ListAPIView

from events_manager.event.forms import EventForm
from events_manager.event.models import Event
from events_manager.event.serializers import EventSerializer
from json import loads
import requests


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('event.add_typeevent',raise_exception=False), name='dispatch')
class EventCreateView(CreateView):
    model = Event
    success_url = reverse_lazy('event:list')
    form_class = EventForm

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('event.view_event',raise_exception=False), name='dispatch')
class EventDetailView(DetailView):
    model = Event

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('event.view_event',raise_exception=False), name='dispatch')
class EventListView(ListView):
    model = Event

    def post(self,request):

        keyword = request.POST.get('keyword')

        events = self.get_queryset()

        events = events.filter(
            Q(name__icontains=keyword)
        )

        return render(
            request,
            'event/event_list.html',
            {
                'object_list' : events,
                'keyword' : keyword
            }
        )

    def get_context_data(self):
        context = super().get_context_data()

        try:
            json_file = open('events_manager/allies_sites.json').read()
            JSON_ALLIES_SITES = loads(json_file)
            sites = JSON_ALLIES_SITES['SITES']
            allies_events = []

            for site in sites:
                response = requests.get(site)
                allies_events += response.json()
                context['allies_events'] = allies_events
        except:
            raise
        
        return context

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('event.add_event',raise_exception=False), name='dispatch')
class EventCreateView(CreateView):
    model = Event
    success_url = reverse_lazy('event:list')
    form_class = EventForm
        

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('event.change_event',raise_exception=False), name='dispatch')
class EventUpdateView(UpdateView):
    model = Event
    success_url = reverse_lazy('event:list')
    form_class = EventForm

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('event.delete_event',raise_exception=False), name='dispatch')
class EventDeleteView(DeleteView):
    model = Event
    success_url = reverse_lazy('event:list')

class EventAPIView(ListAPIView):
    queryset = Event.objects.filter(is_active=True)
    serializer_class = EventSerializer
    