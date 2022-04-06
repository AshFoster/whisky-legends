from django.contrib import admin
from .models import Type, Brand, Country, Region, Flavour, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'type',
        'brand',
        'country',
        'region',
        'flavour',
        'price',
        'rating',
        'image',
    )

    ordering = ('name',)

    def country(self, obj):
        return obj.brand.country
    country.admin_order_field = 'brand__country'

    def region(self, obj):
        return obj.brand.region
    region.admin_order_field = 'brand__region'


class TypeAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class BrandAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class CountryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class RegionAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class FlavourAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Flavour, FlavourAdmin)
