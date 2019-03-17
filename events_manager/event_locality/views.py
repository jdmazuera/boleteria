from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import render
from events_manager.event.models import Event
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from events_manager.event_locality.forms import EventLocalityForm
from events_manager.event_locality.models import EventLocality
from events_manager.locality.models import Locality
from django.contrib.auth.decorators import login_required,permission_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('eventlocality.add_eventlocality',raise_exception=False), name='dispatch')
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

        try:
            event = Event.objects.get(pk=kwargs['event'])
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse_lazy('core:index'))
        
        values = request.POST.dict()

        for key in values:
            key_splited =  key.split('_')
            if len(key_splited) > 1:
                try:
                    locality = Locality.objects.get(pk=key_splited[0])
                except ObjectDoesNotExist:
                    return HttpResponseRedirect(reverse_lazy('event:detail',args=[kwargs['event']]))

                EventLocality.objects.update_or_create(
                    event=event, locality=locality,
                    defaults={key_splited[1]: values[key]},
                )

        return HttpResponseRedirect(reverse_lazy('event:detail',args=[kwargs['event']]))