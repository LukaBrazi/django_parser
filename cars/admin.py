from django.contrib import admin

from cars.models import Car, Brand
from .forms import CarForm


@admin.register(Car)
class Car(admin.ModelAdmin):
    list_display = (f'brand', 'title', 'price_in_usd', 'link')
    search_fields = ('brand.name', 'title')
    form = CarForm


@admin.register(Brand)
class Brand(admin.ModelAdmin):
    list_display = ('name', 'base_url')
