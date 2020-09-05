import django_tables2 as tables
from .models import AvitoData, AvitoPriceChange, AvitoNew


class AvitoTable(tables.Table):
    class Meta:
        model = AvitoData
        template_name = "django_tables2/bootstrap.html"
        fields = ("ad_rooms",
                  "ad_square",
                  "ad_place",
                  "ad_city",
                  "ad_price",
                  "ad_url",
                  "ad_price_delta",
                  "ad_name")


class AvitoChangeTable(tables.Table):
    class Meta:
        model = AvitoPriceChange
        template_name = "django_tables2/bootstrap.html"
        fields = ("avitodata__ad_rooms",
                  "avitodata__ad_square",
                  "avitodata__ad_price",
                  "avitodata__ad_price_delta",
                   "avitodata__ad_city",
                  "avitodata__ad_url",
                  "avitodata__ad_place",
                  "avitodata__ad_name")


class AvitoNewTable(tables.Table):
    class Meta:
        model = AvitoNew
        template_name = "django_tables2/bootstrap.html"
        fields = ("avitodata__ad_rooms",
                  "avitodata__ad_square",
                  "avitodata__ad_price",
                  "avitodata__ad_price_delta",
                  "avitodata__ad_city",

                  "avitodata__ad_url",
                  "avitodata__ad_place",
                  "avitodata__ad_name")
