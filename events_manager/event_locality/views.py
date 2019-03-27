from django.shortcuts import render
from django.views.generic import View,CreateView,UpdateView,ListView,DetailView,DeleteView
from django.http import HttpResponse
from django.shortcuts import render
from events_manager.event.models import Event
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from events_manager.event_locality.forms import EventLocalityForm,EventLocalityFormCRUD
from events_manager.event_locality.models import EventLocality
from events_manager.locality.models import Locality
from django.contrib.auth.decorators import login_required,permission_required
from django.utils.decorators import method_decorator
from django.db.models import Q


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('eventlocality.add_eventlocality',raise_exception=False), name='dispatch')
class EventLocalityAsignView(View):
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
                
                defaults={
                    key_splited[1]: values[key]
                }

                try:
                    obj = EventLocality.objects.get(event=event, locality=locality)
                    for key, value in defaults.items():
                        setattr(obj, key, value)
                    obj.save()
                except ObjectDoesNotExist:
                    new_values = {'event': event, 'locality': locality}
                    new_values.update(defaults)
                    obj = EventLocality(**new_values)
                    obj.save()

        return HttpResponseRedirect(reverse_lazy('event:detail',args=[kwargs['event']]))

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('eventlocality.add_eventlocality',raise_exception=False), name='dispatch')
class EventLocalityCreateView(CreateView):
    model = EventLocality
    success_url = reverse_lazy('eventlocality:list')
    form_class = EventLocalityFormCRUD

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('eventlocality.view_eventlocality',raise_exception=False), name='dispatch')
class EventLocalityListView(ListView):
    model = EventLocality

    def post(self,request):

        keyword = request.POST.get('keyword')

        event_localities = self.get_queryset()

        event_localities = event_localities.filter(
            Q(event__name__icontains=keyword)
            |Q(locality__name__icontains=keyword)
        )

        return render(
            request,
            'event_locality/eventlocality_list.html',
            {
                'object_list' : event_localities,
                'keyword' : keyword
            }
        )

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('eventlocality.delete_eventlocality',raise_exception=False), name='dispatch')
class EventLocalityDeleteView(DeleteView):
    model = EventLocality
    success_url = reverse_lazy('eventlocality:list')

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('eventlocality.change_eventlocality',raise_exception=False), name='dispatch')
class EventLocalityUpdateView(UpdateView):
    model = EventLocality
    success_url = reverse_lazy('eventlocality:list')
    form_class = EventLocalityFormCRUD

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('eventlocality.view_eventlocality',raise_exception=False), name='dispatch')
class EventLocalityDetailView(DetailView):
    model = EventLocality