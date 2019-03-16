from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import render
from events_manager.event.models import Event
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from events_manager.event_locality.forms import EventLocalityForm


class EventLocalityCreateView(View):
    def get(self,request, *args, **kwargs):
        try:
            event = Event.objects.get(pk=kwargs['event'])
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse_lazy('core:index'))

        form = EventLocalityForm(event)

        return render(
            request,
            'event_locality/event_locality_form.html',
            {
                'form' : form
            }
        )

    def post(self,request, *args, **kwargs):
        print('hola',request.POST)
        return HttpResponseRedirect(reverse_lazy('event:detail',args=[kwargs['event']]))