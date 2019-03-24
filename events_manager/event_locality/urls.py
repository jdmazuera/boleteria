from django.contrib import admin
from django.urls import path,include
from events_manager.event_locality.views import EventLocalityAsignView,EventLocalityCreateView,EventLocalityListView,EventLocalityDeleteView,EventLocalityDetailView,EventLocalityUpdateView

app_name = 'eventlocality'

urlpatterns = [
    path('',EventLocalityListView.as_view(),name='list'),
    path('<int:pk>',EventLocalityDetailView.as_view(),name='detail'),
    path('create',EventLocalityCreateView.as_view(),name='create'),
    path('create/<int:event>',EventLocalityAsignView.as_view(),name='create'),
    path('update/<int:pk>',EventLocalityUpdateView.as_view(),name='update'),
    path('delete/<int:pk>',EventLocalityDeleteView.as_view(),name='delete')    
]