"""events_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('core/', include('events_manager.core.urls')),
    path('event/', include('events_manager.event.urls')),
    path('ticket/', include('events_manager.ticket.urls')),
    path('receipt/', include('events_manager.receipt.urls')),
    path('report/', include('events_manager.report.urls')),
    path('type_event/', include('events_manager.type_event.urls')),
    path('locality/', include('events_manager.locality.urls')),
    path('', RedirectView.as_view(url='core/')),
    path('social-auth/', include('social_django.urls', namespace="social"))
]
