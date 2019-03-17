from django.contrib import admin
from django.urls import path,include
from events_manager.type_event.views import TypeEventDetailView, TypeEventListView, TypeEventCreateView, TypeEventUpdateView, TypeEventDeleteView

app_name = 'type_event'

urlpatterns = [
    path('', TypeEventListView.as_view(), name='list'),
    path('<int:pk>', TypeEventDetailView.as_view(), name='detail'),
    path('create',TypeEventCreateView.as_view(),name='create'),
    path('update/<int:pk>',TypeEventUpdateView.as_view(),name='update'),
    path('delete/<int:pk>',TypeEventDeleteView.as_view(),name='delete')
]