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

from events_manager.core.models import User
from events_manager.event.models import Event
from events_manager.event_locality.models import EventLocality
from events_manager.locality.models import Locality
from events_manager.receipt.models import Receipt
from events_manager.ticket.models import Ticket
from events_manager.type_event.models import TypeEvent

from events_manager.ticket.forms import TicketForm

from django.db.models import Q

# Create your views here.
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('ticket.view_ticket',raise_exception=False), name='dispatch')
class TicketDetailView(DetailView):
    model = Ticket

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('ticket.view_ticket',raise_exception=False), name='dispatch')
class TicketListView(ListView):
    model = Ticket

    def post(self,request):
        keyword = request.POST.get('keyword')

        tickets = self.get_queryset()

        tickets = tickets.filter(
            Q(identifier__icontains=keyword)
            |Q(receipt__identifier__icontains=keyword)
            |Q(receipt__costumer__first_name__icontains=keyword)
            |Q(receipt__costumer__last_name__icontains=keyword)
            |Q(receipt__costumer__identification__icontains=keyword)
            |Q(event_locality__event__name__icontains=keyword)
            |Q(event_locality__locality__name__icontains=keyword)
        )

        return render(
            request,
            'ticket/ticket_list.html',
            {
                'object_list': tickets,
                'keyword' : keyword
            }
        )

    def get_queryset(self):
        if self.request.user.has_perm('ticket.view_all_tickets'):
            tickets = Ticket.objects.filter(receipt__confirmed=True,is_active=True,receipt__is_active=True)
        else:
            tickets = Ticket.objects.filter(receipt__costumer=self.request.user,receipt__confirmed=True,is_active=True,receipt__is_active=True)
        return tickets

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('ticket.add_ticket',raise_exception=False), name='dispatch')
class TicketCreateView(CreateView):
    model = Ticket
    success_url = reverse_lazy('ticket:list')
    form_class = TicketForm

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('ticket.change_ticket',raise_exception=False), name='dispatch')
class TicketUpdateView(UpdateView):
    model = Ticket
    success_url = reverse_lazy('ticket:list')
    form_class = TicketForm

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('ticket.delete_ticket',raise_exception=False), name='dispatch')
class TicketDeleteView(DeleteView):
    model = Ticket
    success_url = reverse_lazy('ticket:list')
    fields = ['name']
    template_name_suffix = '_confirm_delete'