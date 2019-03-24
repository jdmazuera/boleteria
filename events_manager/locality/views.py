from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required,permission_required
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView

from events_manager.locality.forms import LocalityForm
from events_manager.locality.models import Locality

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('locality.view_locality',raise_exception=False), name='dispatch')
class LocalityDetailView(DetailView):
    model = Locality

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('locality.view_locality',raise_exception=False), name='dispatch')
class LocalityListView(ListView):
    model = Locality

    def post(self,request):

        keyword = request.POST.get('keyword')

        localities = self.get_queryset()

        localities = localities.filter(
            Q(name__icontains=keyword)
            |Q(event_type__name__icontains=keyword)
        )

        return render(
            request,
            'locality/locality_list.html',
            {
                'object_list' : localities,
                'keyword' : keyword
            }
        )

    def get_queryset(self):
        query_set =  Locality.objects.filter(is_active=True)
        return query_set

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('locality.add_locality',raise_exception=False), name='dispatch')
class LocalityCreateView(CreateView):
    model = Locality
    success_url = reverse_lazy('locality:list')
    form_class = LocalityForm

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('locality.change_locality',raise_exception=False), name='dispatch')
class LocalityUpdateView(UpdateView):
    model = Locality
    success_url = reverse_lazy('locality:list')
    form_class = LocalityForm

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('locality.delete_locality',raise_exception=False), name='dispatch')
class LocalityDeleteView(DeleteView):
    model = Locality
    success_url = reverse_lazy('locality:list')
    template_name_suffix = '_confirm_delete'