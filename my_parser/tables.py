import django_tables2 as tables
from .models import AvitoData


class AvitoTable(tables.Table):
    class Meta:
        model = AvitoData
        template_name = "django_tables2/bootstrap.html"
        fields = ("ad_rooms", "ad_square", "ad_price", "ad_url","ad_place",  "ad_price_delta",  "ad_name")
