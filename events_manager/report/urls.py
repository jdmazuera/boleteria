from django.urls import path,include
from events_manager.report.views import sell_by_event

app_name = 'report'

urlpatterns = [
    path('sell_by_event', sell_by_event, name='sell_by_event')
]