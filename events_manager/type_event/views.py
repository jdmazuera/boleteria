from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required,permission_required
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView

from events_manager.type_event.forms import TypeEventForm
from events_manager.type_event.models import TypeEvent

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('typeevent.view_typeevent',raise_exception=False), name='dispatch')
class TypeEventDetailView(DetailView):
    model = TypeEvent

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('typeevent.view_typeevent',raise_exception=False), name='dispatch')
class TypeEventListView(ListView):
    model = TypeEvent

    def post(self,request):
        keyword = request.POST.get('keyword')

        query_set = self.get_queryset()

        query_set = query_set.filter(
            Q(name__icontains=keyword)
        )

        return render(
            request,
            'type_event/typeevent_list.html',
            {
                'object_list': query_set,
                'keyword' : keyword
            }
        )

    def get_queryset(self):
        query_set = TypeEvent.objects.filter(is_active=True)
        return query_set

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('typeevent.add_typeevent',raise_exception=False), name='dispatch')
class TypeEventCreateView(CreateView):
    model = TypeEvent
    success_url = reverse_lazy('type_event:list')
    form_class = TypeEventForm

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('typeevent.change_typeevent',raise_exception=False), name='dispatch')
class TypeEventUpdateView(UpdateView):
    model = TypeEvent
    success_url = reverse_lazy('type_event:list')
    form_class = TypeEventForm

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('typeevent.delete_typeevent',raise_exception=False), name='dispatch')
class TypeEventDeleteView(DeleteView):
    model = TypeEvent
    success_url = reverse_lazy('type_event:list')
    template_name_suffix = '_confirm_delete'