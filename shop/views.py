import math
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Min, Max
from django.db.models.functions import Lower
from django.views import generic, View
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
    sort = None
    direction = None
    price_min = 0
    price_max = 0
    price_min_initial = 0
    price_max_initial = 0
    products_filtered = False
    search_query = None

    def get_queryset(self):
        sort_by = self.request.GET.get('sort')
        sort_direction = self.request.GET.get('direction')
        type_filter = self.request.GET.get('type')
        brand_filter = self.request.GET.get('brand')
        country_filter = self.request.GET.get('country')
        region_filter = self.request.GET.get('region')
        flavour_filter = self.request.GET.get('flavour')
        age_filter = self.request.GET.get('age')
        price_filter = self.request.GET.get('price')
        self.search_query = self.request.GET.get('search')

        if sort_by:
            self.sort = sort_by
            if sort_by == 'brand':
                sort_by = 'lower_brand'
                self.queryset = self.queryset.annotate(
                    lower_brand=Lower('brand__friendly_name'))

            if sort_direction:
                self.direction = sort_direction
                if sort_direction == 'desc':
                    sort_by = f'-{sort_by}'
            self.queryset = self.queryset.order_by(sort_by)

        if type_filter:
            self.products_filtered = True
            self.queryset = self.queryset.filter(
                type__name=type_filter)

        if brand_filter:
            self.products_filtered = True
            self.queryset = self.queryset.filter(
                brand__name=brand_filter)

        if country_filter:
            self.products_filtered = True
            self.queryset = self.queryset.filter(
                brand__country__name=country_filter)

        if region_filter:
            self.products_filtered = True
            self.queryset = self.queryset.filter(
                brand__region__name=region_filter)

        if flavour_filter:
            self.products_filtered = True
            self.queryset = self.queryset.filter(
                flavour__name=flavour_filter)

        if age_filter:
            self.products_filtered = True
            self.queryset = self.queryset.filter(
                age=age_filter)

        self.price_min_initial = int(math.floor(
            self.queryset.aggregate(Min('price'))['price__min']))
        self.price_max_initial = int(math.ceil(
            self.queryset.aggregate(Max('price'))['price__max']))

        if price_filter:
            self.products_filtered = True
            price_range = price_filter.split(',')
            try:
                self.price_min = int(float(price_range[0]))
                self.price_max = int(float(price_range[1]))
            except ValueError:
                self.price_min = self.price_min_initial
                self.price_max = self.price_max_initial

            self.queryset = self.queryset.filter(
                price__range=(self.price_min, self.price_max))

        if not self.search_query:
            messages.error(
                self.request,
                "You didn't enter any search criteria!"
            )
            return self.queryset

        queries = (Q(name__icontains=self.search_query) |
                   Q(brand__friendly_name__icontains=self.search_query) |
                   Q(age__icontains=self.search_query))
        self.queryset = self.queryset.filter(queries)

        return self.queryset

    def get_context_data(self, **kwargs):
        """
        Sets context data to be used on shop.html
        """
        context = super(Shop, self).get_context_data(**kwargs)

        products_sorted = self.request.GET.get('sort')
        types_filtered = self.request.GET.get('type')
        brands_filtered = self.request.GET.get('brand')
        countries_filtered = self.request.GET.get('country')
        regions_filtered = self.request.GET.get('region')
        flavours_filtered = self.request.GET.get('flavour')
        ages_filtered = self.request.GET.get('age')
        prices_filtered = self.request.GET.get('price')

        current_sorting = f'{self.sort}_{self.direction}'
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
        ages = {}
        ages_count = 0

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

            if product.brand.region:
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

            if product.age:
                if product.age not in ages:
                    ages[product.age] = 1
                    ages_count += 1
                else:
                    ages[product.age] = ages[product.age] + 1

        context['current_sorting'] = current_sorting
        context['products_sorted'] = products_sorted
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
        context['ages'] = ages
        context['ages_count'] = ages_count
        context['ages_filtered'] = ages_filtered
        context['price_min'] = self.price_min
        context['price_max'] = self.price_max
        context['price_min_initial'] = self.price_min_initial
        context['price_max_initial'] = self.price_max_initial
        context['prices_filtered'] = prices_filtered
        context['products_filtered'] = self.products_filtered
        context['search_query'] = self.search_query

        return context


class ProductDetail(View):
    """
    Product Detail class based view to show individual Product model
    objects on product_detail.html
    """
    def get(self, request, product_id, *args, **kwargs):
        queryset = Product.objects.all()
        product = get_object_or_404(queryset, pk=product_id)

        return render(
            request,
            'shop/product_detail.html',
            {
                'product': product,
            },
        )
