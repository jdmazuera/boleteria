from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth import authenticate, login as login_django, logout as logout_django
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.forms import Form
from django.db.models import Q
from json import dumps

from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic import TemplateView,View

from events_manager.core.forms import UserFrom,RegistroForm
from events_manager.core.models import User

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('core.view_user',raise_exception=False), name='dispatch')
class UserDetailView(DetailView):
    model = User

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('core.view_user',raise_exception=False), name='dispatch')
class UserListView(ListView):
    model = User

    def post(self,request):
        keyword = request.POST.get('keyword')

        users = self.get_queryset()

        users = users.filter(
            Q(first_name__icontains=keyword)
            |Q(last_name__icontains=keyword)
            |Q(identification__icontains=keyword)
            |Q(position__icontains=keyword)
        )

        return render(
            request,
            'core/user_list.html',
            {
                'object_list' : users,
                'keyword' : keyword
            }
        )

    def get_queryset(self):
        query_set =  User.objects.filter(is_active=True)
        return query_set
        

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('core.add_user',raise_exception=False), name='dispatch')
class UserCreateView(CreateView):
    model = User
    success_url = reverse_lazy('core:list')
    form_class = UserFrom

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('core.change_user',raise_exception=False), name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    success_url = reverse_lazy('core:list')
    form_class = UserFrom

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('core.delete_user',raise_exception=False), name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('core:list')

@method_decorator(login_required, name='dispatch')
class IndexView(TemplateView):
    template_name = 'core/index.html'

class RegistroView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return render(request,'core/registro.html',{
            'form' : RegistroForm()
        })
    def post(self, request, *args, **kwargs):
        usuario = RegistroForm(request.POST)
        
        if usuario.is_valid():
            usuario.save()
            return redirect('core:login')
        else:
            return render(request,'core/registro.html',{
                'form' : usuario
            })

class LoginView(View):
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('core:index')
        return render(
            request,
            'core/login.html',
            {
                'next': request.GET.get('next')
            }
        )
    def post(self,request,*args,**kwargs):
        if request.GET:
            next = request.GET.get('next')
        else:
            next = None
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None and user.is_active:
            login_django(request,user)
            receipt = user.receipt_set.all().order_by('-creation_date').first()
            if receipt and not receipt.confirmed:
                shopping_car = {}
                shopping_car['receipt_session_id'] = receipt.id
                shopping_car['receipt_items_quantity'] = receipt.quantity
                request.session['shopping_car'] = dumps(shopping_car)
            if next:
                return HttpResponseRedirect(next)
            return redirect('core:index')

        return render(
            request,
            'core/login.html',
            {
                'next': request.GET.get('next'),
                'mostrar_error_login' : True
            }
        )
    
@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    def get(self,request,*args,**kwargs):
        logout_django(request)
        return redirect('core:login')