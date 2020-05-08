from django.contrib import admin

from cars.models import Car
from .forms import CarForm


@admin.register(Car)
class Car(admin.ModelAdmin):
    list_display = ('title', 'price_in_usd', 'link')
    form = CarForm
