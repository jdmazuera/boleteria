from django.contrib import admin
from django.urls import path,include
from events_manager.event.views import (
        EventDetailView, EventListView, EventCreateView, EventUpdateView, EventDeleteView
    )

urlpatterns = [
    path('', EventListView.as_view(), name='list'),
    path('<int:pk>', EventDetailView.as_view(), name='detail'),
    path('create',EventCreateView.as_view(),name='create'),
    path('update/<int:pk>',EventUpdateView.as_view(),name='update'),
    path('delete/<int:pk>',EventDeleteView.as_view(),name='delete')
]