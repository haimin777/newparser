from django.db import models

# Create your models here.

class AvitoData(models.Model):

    ad_id = models.IntegerField()
    ad_name = models.CharField(max_length=200)
    ad_url = models.URLField()
    ad_price = models.IntegerField()
    ad_place = models.CharField(max_length=300)
    ad_price_delta = models.IntegerField(default=0)

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





