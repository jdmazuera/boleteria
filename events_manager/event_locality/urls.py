from django.contrib import admin
from django.urls import path,include
from events_manager.event_locality.views import EventLocalityCreateView

app_name = 'eventlocality'

urlpatterns = [
    path('create/<int:event>',EventLocalityCreateView.as_view(),name='create')
]