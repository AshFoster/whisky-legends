from django.contrib import admin
from .models import Type, Brand, Country, Region, Product

admin.site.register(Type)
admin.site.register(Brand)
admin.site.register(Country)
admin.site.register(Region)
admin.site.register(Product)
