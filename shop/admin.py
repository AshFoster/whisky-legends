from django.contrib import admin
from .models import Type, Brand, Country, Region, Flavour, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('brand_friendly', 'name', 'type',
                    'country', 'region', 'flavour',
                    'price', 'abv', 'volume','rating',
                    'image',)

    ordering = ('brand',)

    def brand_friendly(self, obj):
        if obj.brand:
            return obj.brand.friendly_name
        else:
            return None
    brand_friendly.short_description = 'Brand'

    def country(self, obj):
        if obj.brand.country:
            return obj.brand.country.friendly_name
        else:
            return None
    country.admin_order_field = 'brand__country'

    def region(self, obj):
        if obj.brand.region:
            return obj.brand.region.friendly_name
        else:
            return None
    region.admin_order_field = 'brand__region'

    def rating(self, obj):
        return obj.calc_rating()
    brand_friendly.short_description = 'Rating'


class TypeAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
    )
    exclude = ('name',)


class BrandAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
    )
    exclude = ('name',)


class CountryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
    )
    exclude = ('name',)


class RegionAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
    )
    exclude = ('name',)


class FlavourAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
    )
    exclude = ('name',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Flavour, FlavourAdmin)
