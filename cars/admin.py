from django.contrib import admin
from cars.models import Car, Brand
from .forms import CarForm
from .models import Brand as BrandModel
from django.core import management


@admin.register(Car)
class Car(admin.ModelAdmin):
    list_display = (f'brand', 'title', 'price_in_usd', 'link')
    list_filter = ('brand',)
    search_fields = ('brand', 'title')
    form = CarForm


@admin.register(Brand)
class Brand(admin.ModelAdmin):
    list_display = ('name', 'base_url')

    def run_parser(self, request, queryset):
        for brand in queryset:
            brand = BrandModel.objects.get(name=brand)
            management.call_command('autoria_parser', brand=brand.name, base_url=brand.base_url)
            self.message_user(request, f"Parsing for {brand} complete")

    run_parser.short_description = "Run parser for selected brand"
    actions = [run_parser]
