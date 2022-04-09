from django.contrib import messages
from django.db.models import Q
from django.views import generic
from .models import Product


class Shop(generic.ListView):
    """
    Shop class based view to show all products, including
    filtering, sorting and search queries
    """
    model = Product
    queryset = Product.objects.all()
    template_name = 'shop/shop.html'
    context_object_name = 'products'

    def get_queryset(self):
        type_filter = self.request.GET.get('type')
        brand_filter = self.request.GET.get('brand')
        country_filter = self.request.GET.get('country')
        region_filter = self.request.GET.get('region')
        flavour_filter = self.request.GET.get('flavour')
        search_query = self.request.GET.get('search')

        if type_filter:
            self.queryset = self.queryset.filter(
                type__name=type_filter)

        if brand_filter:
            self.queryset = self.queryset.filter(
                brand__name=brand_filter)

        if country_filter:
            self.queryset = self.queryset.filter(
                brand__country__name=country_filter)

        if region_filter:
            self.queryset = self.queryset.filter(
                brand__region__name=region_filter)

        if flavour_filter:
            self.queryset = self.queryset.filter(
                flavour__name=flavour_filter)

        if not search_query:
            messages.error(
                self.request,
                "You didn't enter any search criteria!"
            )
            return self.queryset

        queries = (Q(name__icontains=search_query) |
                   Q(brand__friendly_name__icontains=search_query) |
                   Q(age__icontains=search_query))
        self.queryset = self.queryset.filter(queries)

        return self.queryset

    def get_context_data(self, **kwargs):
        """
        Sets context data to be used on shop.html
        """
        context = super(Shop, self).get_context_data(**kwargs)

        types_filtered = self.request.GET.get('type')
        brands_filtered = self.request.GET.get('brand')
        countries_filtered = self.request.GET.get('country')
        regions_filtered = self.request.GET.get('region')
        flavours_filtered = self.request.GET.get('flavour')

        types = {}
        type_names = {}
        types_count = 0
        brands = {}
        brand_names = {}
        brands_count = 0
        countries = {}
        country_names = {}
        countries_count = 0
        regions = {}
        region_names = {}
        regions_count = 0
        flavours = {}
        flavour_names = {}
        flavours_count = 0

        for product in self.queryset:
            if product.type.friendly_name not in types:
                type_names[product.type.friendly_name] = product.type.name
                types[product.type.friendly_name] = 1
                types_count += 1
            else:
                types[product.type.friendly_name] = types[
                        product.type.friendly_name] + 1

            if product.brand.friendly_name not in brands:
                brand_names[product.brand.friendly_name] = product.brand.name
                brands[product.brand.friendly_name] = 1
                brands_count += 1
            else:
                brands[product.brand.friendly_name] = brands[
                    product.brand.friendly_name] + 1

            if product.brand.country.friendly_name not in countries:
                country_names[product.brand.country.friendly_name] = \
                    product.brand.country.name
                countries[product.brand.country.friendly_name] = 1
                countries_count += 1
            else:
                countries[product.brand.country.friendly_name] = countries[
                    product.brand.country.friendly_name] + 1

            if product.brand.region.friendly_name not in regions:
                region_names[product.brand.region.friendly_name] = \
                    product.brand.region.name
                regions[product.brand.region.friendly_name] = 1
                regions_count += 1
            else:
                regions[product.brand.region.friendly_name] = regions[
                    product.brand.region.friendly_name] + 1

            if product.flavour.friendly_name not in flavours:
                flavour_names[product.flavour.friendly_name] = \
                    product.flavour.name
                flavours[product.flavour.friendly_name] = 1
                flavours_count += 1
            else:
                flavours[product.flavour.friendly_name] = flavours[
                    product.flavour.friendly_name] + 1

        context['types'] = types
        context['type_names'] = type_names
        context['types_count'] = types_count
        context['types_filtered'] = types_filtered
        context['brands'] = brands
        context['brand_names'] = brand_names
        context['brands_count'] = brands_count
        context['brands_filtered'] = brands_filtered
        context['countries'] = countries
        context['country_names'] = country_names
        context['countries_count'] = countries_count
        context['countries_filtered'] = countries_filtered
        context['regions'] = regions
        context['region_names'] = region_names
        context['regions_count'] = regions_count
        context['regions_filtered'] = regions_filtered
        context['flavours'] = flavours
        context['flavour_names'] = flavour_names
        context['flavours_count'] = flavours_count
        context['flavours_filtered'] = flavours_filtered

        return context
