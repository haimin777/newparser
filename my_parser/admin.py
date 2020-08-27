from django.contrib import admin

# Register your models here.
from .models import AvitoData, AvitoPriceChange, AvitoNew

admin.site.register(AvitoData)
admin.site.register(AvitoPriceChange)
admin.site.register(AvitoNew)