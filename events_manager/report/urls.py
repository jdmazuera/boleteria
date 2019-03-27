from django.urls import path,include
from events_manager.report.views import sell_by_event,top_costumers,summerize_event_locality

app_name = 'report'

urlpatterns = [
    path('sell_by_event', sell_by_event, name='sell_by_event'),
    path('top_costumers', top_costumers, name='top_costumers'),
    path('summerize_event_locality', summerize_event_locality, name='summerize_event_locality')
]