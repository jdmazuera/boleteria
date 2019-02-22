from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth import authenticate, login as login_django, logout as logout_django
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.forms import Form

from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic import TemplateView

from events_manager.core.forms import UserFrom,RegistroForm
from events_manager.core.models import User

@method_decorator(login_required, name='dispatch')
class UserDetailView(DetailView):
    model = User
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('user.view_user',raise_exception=False), name='dispatch')
class UserListView(ListView):
    model = User

    def get_context_data(self,**kwargs):
        print(self.http_method_names)
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('user.create_user',raise_exception=False), name='dispatch')
class UserCreateView(CreateView):
    model = User
    success_url = reverse_lazy('core:list')
    form_class = UserFrom
    verbose_name = 'Crear'
    model_name = 'Usuarios'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['view_name'] = self.verbose_name
        context['model'] = self.model_name
        return context

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('user.edit_user',raise_exception=False), name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    success_url = reverse_lazy('core:list')
    form_class = UserFrom
    template_name_suffix = '_update_form'
    verbose_name = 'Editar'
    model_name = 'Usuarios'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['view_name'] = self.verbose_name
        context['model'] = self.model_name
        return context

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('user.delete_user',raise_exception=False), name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('list')
    fields = ['username','email','password']
    template_name_suffix = '_confirm_delete'


@method_decorator(login_required, name='dispatch')
class IndexView(TemplateView):
    template_name = 'core/index.html'

def registro(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.POST:
        #print(request.POST)
        usuario = RegistroForm(request.POST)
        
        if usuario.is_valid():
            usuario.save()
            return redirect('core:login')
        else:
            return render(request,'core/registro.html',{
                'form' : usuario
            })

    return render(request,'core/registro.html',{
        'form' : RegistroForm()
    })


def login(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.POST:
        if request.GET:
            next = request.GET.get('next')
        else:
            next = None
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login_django(request,user)
            if next:
                return HttpResponseRedirect(next)
            return redirect('core:index')
        else:
            return render(request,'core/login.html',{
                'next': request.GET.get('next'),
                'mostrar_error_login' : True
            })

    return render(request,'core/login.html',{
        'next': request.GET.get('next')
    })

@login_required
def logout(request):
    logout_django(request)
    return redirect('core:login')

@login_required
def users_index(request):
    from events_manager.core.models import User
    users =  User.objects.all()
    return render(request,'core/users.html',{
        'users':users
    })