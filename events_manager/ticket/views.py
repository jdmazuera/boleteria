from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required,permission_required
from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic import TemplateView

from events_manager.ticket.forms import TicketForm
from events_manager.ticket.models import Ticket
from events_manager.event.models import Event

from django.db.models import Q

# Create your views here.
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('ticket.view_ticket',raise_exception=False), name='dispatch')
class TicketDetailView(DetailView):
    model = Ticket
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('ticket.view_ticket',raise_exception=False), name='dispatch')
class TicketListView(ListView):
    model = Ticket

    def post(self,request):
        keyword = request.POST.get('keyword')

        if request.user.has_perm('ticket.view_own_ticket'):
            tickets = Ticket.objects.filter(propietario=request.user)
        else:
            tickets = Ticket.objects.all()

        tickets = Ticket.objects.filter(
            Q(event__equipo_local__icontains=keyword)|
            Q(event__equipo_visitante__icontains=keyword)|
            Q(event__name__icontains=keyword)|
            Q(propietario__first_name__icontains=keyword)|
            Q(propietario__last_name__icontains=keyword)|
            Q(propietario__identification__icontains=keyword)
        )

        return render(
            request,
            'ticket/ticket_list.html',
            {
                'tickets': tickets
            }
        )

    def get_queryset(self):
        if self.request.user.has_perm('ticket.view_own_ticket'):
            tickets = Ticket.objects.filter(propietario=self.request.user)
        else:
            tickets = Ticket.objects.all()
        return tickets

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('ticket.add_ticket',raise_exception=False), name='dispatch')
class TicketCreateView(CreateView):
    model = Ticket
    form_class = TicketForm
    verbose_name = 'Comprar'
    model_name = 'Boletos'

    def get(self, request, *args, **kwargs):
        if request.GET:
            parent_event_pk = request.GET.get('event')
            if parent_event_pk:
                try:
                    event = Event.objects.get(pk=parent_event_pk)
                    self.form_class.base_fields['event'].initial = event.pk
                    self.form_class.base_fields['price'].initial = event.precio_ticket
                    self.form_class.base_fields['date'].initial = event.date
                    self.form_class.base_fields['propietario'].initial = request.user.id
                except:
                    pass

            if not request.user.has_perm('ticket.change_ticket'):
                for key in self.form_class.base_fields:
                    if not key == 'metodo_pago':
                        self.form_class.base_fields[key].disabled = True

        return super().get(request, *args, **kwargs)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['view_name'] = self.verbose_name
        context['model'] = self.model_name
        return context

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('ticket.change_ticket',raise_exception=False), name='dispatch')
class TicketUpdateView(UpdateView):
    model = Ticket
    success_url = reverse_lazy('ticket:list')
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
@method_decorator(permission_required('ticket.delete_ticket',raise_exception=False), name='dispatch')
class TicketDeleteView(DeleteView):
    model = Ticket
    success_url = reverse_lazy('ticket:list')
    fields = ['name']
    template_name_suffix = '_confirm_delete'

@login_required
@permission_required('ticket.view_ticket',raise_exception=False)
def quote(request,ticket_pk):

    ticket = Ticket.objects.get(pk=ticket_pk)

    return render(
        request,
        'ticket/ticket_quote.html',
        {
            'object' : ticket
        }
    )