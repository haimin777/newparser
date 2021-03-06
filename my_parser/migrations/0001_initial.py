# Generated by Django 3.1 on 2020-08-24 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AvitoData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad_id', models.IntegerField()),
                ('ad_name', models.CharField(max_length=200)),
                ('ad_url', models.URLField()),
                ('ad_price', models.IntegerField()),
                ('ad_place', models.CharField(max_length=300)),
                ('ad_price_delta', models.IntegerField(default=0)),
            ],
        ),
    ]
