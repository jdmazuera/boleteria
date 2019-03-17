from django.contrib import admin
from django.urls import path,include
from events_manager.locality.views import LocalityDetailView, LocalityListView, LocalityCreateView, LocalityUpdateView, LocalityDeleteView

app_name = 'locality'

urlpatterns = [
    path('', LocalityListView.as_view(), name='list'),
    path('<int:pk>', LocalityDetailView.as_view(), name='detail'),
    path('create',LocalityCreateView.as_view(),name='create'),
    path('update/<int:pk>',LocalityUpdateView.as_view(),name='update'),
    path('delete/<int:pk>',LocalityDeleteView.as_view(),name='delete')
]