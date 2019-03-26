from rest_framework import serializers
from django.contrib.sites.models import Site
from events_manager.event.models import Event

class EventSerializer(serializers.ModelSerializer):

    nombre = serializers.SerializerMethodField()
    fecha = serializers.SerializerMethodField()
    lugar = serializers.SerializerMethodField()
    hora = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    valor_max = serializers.SerializerMethodField()
    valor_min = serializers.SerializerMethodField()

    def get_nombre(self,obj):
        return obj.name

    def get_fecha(self,obj):
        return obj.date.strftime('%Y-%m-%d')
    
    def get_lugar(self,obj):
        return obj.address
    
    def get_hora(self,obj):
        return obj.date.strftime('%H:%M')

    def get_url(self,obj):
        site = Site.objects.get_current()
        return 'http://'+site.domain + str(obj.get_absolute_detail_url)
    
    def get_valor_max(self,obj):
        return obj.max_price

    def get_valor_min(self,obj):
        return obj.min_price


    class Meta:
        model = Event
        fields = ('nombre', 'fecha', 'lugar', 'hora','url', 'valor_max', 'valor_min')