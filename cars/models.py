from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=255, verbose_name='Brand name', primary_key=True)
    base_url = models.URLField(verbose_name='Base URL')

    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.name


class Car(models.Model):
    title = models.CharField(max_length=255, verbose_name='Car title')
    price_in_usd = models.CharField(max_length=255, verbose_name='Price in USD')
    price_in_uah = models.CharField(max_length=255, verbose_name='Price in UAH')
    location = models.CharField(max_length=255, verbose_name='Location of car')
    range = models.CharField(max_length=255, verbose_name='Car range')
    link = models.URLField(verbose_name="Link for Car", unique=True)
    brand = models.ForeignKey(Brand, default='Other', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'
