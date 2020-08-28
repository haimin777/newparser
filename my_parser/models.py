from django.db import models

# Create your models here.

class AvitoData(models.Model):

    ad_id = models.IntegerField(verbose_name="Номер")
    ad_name = models.CharField(max_length=200, verbose_name="Название")
    ad_rooms = models.CharField(max_length=100, default='1', verbose_name="Комнаты")
    ad_square = models.CharField(max_length=120, default='2', verbose_name="Площадь")
    ad_url = models.URLField(verbose_name="Ссылка")
    ad_price = models.IntegerField(verbose_name="Цена")
    ad_place = models.CharField(max_length=300, verbose_name="Адрес")
    ad_price_delta = models.IntegerField(default=0, verbose_name="Дельта")

    def __str__(self):

        return self.ad_place

class AvitoPriceChange(models.Model):

    avitodata = models.ForeignKey(AvitoData, on_delete=models.CASCADE)

    def __str__(self):

        return self.avitodata.ad_place

class AvitoNew(models.Model):

    avitodata = models.ForeignKey(AvitoData, on_delete=models.CASCADE)

    def __str__(self):

        return self.avitodata.ad_place





