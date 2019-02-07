from django.contrib import admin
from django.urls import path,include
from events_manager.core.views import (
    IndexView, login, UserDetailView, UserListView, UserCreateView, UserUpdateView, UserDeleteView
    )

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login', login, name='login'),
    path('user/', UserListView.as_view(), name='list'),
    path('user/<int:pk>', UserDetailView.as_view(), name='detail'),
    path('user/create',UserCreateView.as_view(),name='create'),
    path('user/update/<int:pk>',UserUpdateView.as_view(),name='update'),
    path('user/delete/<int:pk>',UserDeleteView.as_view(),name='delete')
]