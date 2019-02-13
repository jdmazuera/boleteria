from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic import TemplateView

from events_manager.ticket.forms import TicketForm
from events_manager.ticket.models import Ticket

# Create your views here.
@method_decorator(login_required, name='dispatch')
class TicketDetailView(DetailView):
    model = Ticket
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context

@method_decorator(login_required, name='dispatch')
class TicketListView(ListView):
    model = Ticket
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['tickets'] = Ticket.objects.all()
        return context

@method_decorator(login_required, name='dispatch')
class TicketCreateView(CreateView):
    model = Ticket
    success_url = reverse_lazy('list')
    form_class = TicketForm
    verbose_name = 'Crear'
    model_name = 'Tickets'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['view_name'] = self.verbose_name
        context['model'] = self.model_name
        return context

@method_decorator(login_required, name='dispatch')
class TicketUpdateView(UpdateView):
    model = Ticket
    success_url = reverse_lazy('list')
    form_class = TicketForm
    template_name_suffix = '_update_form'
    verbose_name = 'Editar'
    model_name = 'Tickets'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['view_name'] = self.verbose_name
        context['model'] = self.model_name
        return context

@method_decorator(login_required, name='dispatch')
class TicketDeleteView(DeleteView):
    model = Ticket
    success_url = reverse_lazy('list')
    fields = ['name']
    template_name_suffix = '_confirm_delete'