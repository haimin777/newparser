from rest_framework import serializers
from .models import AvitoData



class AvitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvitoData
        fields = ('ad_id',
                  'ad_name',
                  'ad_url',
                  'ad_price',
                  'ad_price_delta')