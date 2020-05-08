from django.db import models


class Car(models.Model):
    title = models.CharField(max_length=255, verbose_name='Car title')
    price_in_usd = models.CharField(max_length=255, verbose_name='Price in USD')
    price_in_uah = models.CharField(max_length=255, verbose_name='Price in UAH')
    location = models.CharField(max_length=255, verbose_name='Location of car')
    range = models.CharField(max_length=255, verbose_name='Car range')
    link = models.URLField(verbose_name="Link for Car")

    class Meta:
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'
