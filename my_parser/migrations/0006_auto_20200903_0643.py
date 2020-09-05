# Generated by Django 3.1 on 2020-09-03 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_parser', '0005_auto_20200827_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='avitodata',
            name='ad_city',
            field=models.CharField(default='Пока ничего', max_length=100, verbose_name='Город/Район'),
        ),
        migrations.AlterField(
            model_name='avitodata',
            name='ad_id',
            field=models.IntegerField(verbose_name='Номер'),
        ),
        migrations.AlterField(
            model_name='avitodata',
            name='ad_name',
            field=models.CharField(max_length=200, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='avitodata',
            name='ad_place',
            field=models.CharField(max_length=300, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='avitodata',
            name='ad_price',
            field=models.IntegerField(verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='avitodata',
            name='ad_price_delta',
            field=models.IntegerField(default=0, verbose_name='Дельта'),
        ),
        migrations.AlterField(
            model_name='avitodata',
            name='ad_rooms',
            field=models.CharField(default='1', max_length=100, verbose_name='Комнаты'),
        ),
        migrations.AlterField(
            model_name='avitodata',
            name='ad_square',
            field=models.CharField(default='2', max_length=120, verbose_name='Площадь'),
        ),
        migrations.AlterField(
            model_name='avitodata',
            name='ad_url',
            field=models.URLField(verbose_name='Ссылка'),
        ),
    ]