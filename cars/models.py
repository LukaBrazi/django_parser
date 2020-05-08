from django.db import models


class Car(models.Model):
    title = models.CharField(max_length=255)
    price_in_usd = models.CharField(max_length=255)
    price_in_uah = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    range = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
