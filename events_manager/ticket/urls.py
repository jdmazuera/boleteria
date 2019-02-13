from django.contrib import admin
from django.urls import path,include
from events_manager.ticket.views import (
        TicketDetailView, TicketListView, TicketCreateView, TicketUpdateView, TicketDeleteView
    )

app_name = 'ticket'

urlpatterns = [
    path('', TicketListView.as_view(), name='list'),
    path('<int:pk>', TicketDetailView.as_view(), name='detail'),
    path('create',TicketCreateView.as_view(),name='create'),
    path('update/<int:pk>',TicketUpdateView.as_view(),name='update'),
    path('delete/<int:pk>',TicketDeleteView.as_view(),name='delete')
]