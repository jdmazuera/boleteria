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
from django.views.generic import TemplateView

from events_manager.event.forms import EventForm
from events_manager.event.models import Event

# Create your views here.
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('event.view_event',raise_exception=False), name='dispatch')
class EventDetailView(DetailView):
    model = Event
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('event.view_event',raise_exception=False), name='dispatch')
class EventListView(ListView):
    model = Event

    def post(self,request):
        keyword = request.POST.get('keyword')
        return render(
            request,
            'event/event_list.html',
            {
                'events':Event.objects.filter(Q(name__icontains=keyword)|Q(equipo_local__icontains=keyword)|Q(equipo_visitante__icontains=keyword))
            }
        )

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = Event.objects.filter(is_active=True)
        return context

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('event.add_event',raise_exception=False), name='dispatch')
class EventCreateView(CreateView):
    model = Event
    success_url = reverse_lazy('event:list')
    form_class = EventForm
    verbose_name = 'Crear'
    model_name = 'Eventos'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['view_name'] = self.verbose_name
        context['model'] = self.model_name
        return context

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('event.change_event',raise_exception=False), name='dispatch')
class EventUpdateView(UpdateView):
    model = Event
    success_url = reverse_lazy('event:list')
    form_class = EventForm
    template_name_suffix = '_update_form'
    verbose_name = 'Editar'
    model_name = 'Eventos'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['view_name'] = self.verbose_name
        context['model'] = self.model_name
        return context

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('event.delete_event',raise_exception=False), name='dispatch')
class EventDeleteView(DeleteView):
    model = Event
    success_url = reverse_lazy('event:list')
    fields = ['name']
    template_name_suffix = '_confirm_delete'