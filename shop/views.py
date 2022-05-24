import math
from django.shortcuts import (render, get_object_or_404,
                              redirect, reverse, HttpResponse)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Min, Max, F, Count, Sum
from django.db.models.functions import Lower, Coalesce
from django.views import generic
from profiles.models import UserWishlist
from .models import Product, Review
from .forms import ReviewForm, ProductForm


class Shop(generic.ListView):
    """
    Shop class based view to show all products, including
    filtering, sorting and search queries
    """
    model = Product
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

    def dispatch(self, request, *args, **kwargs):
        '''
        Overides dispatch to check whether the user has submitted
        a blank search and makes them aware if they have.
        '''
        if 'search' in self.request.GET:
            self.search_query = self.request.GET.get('search')
            if not self.search_query:
                messages.warning(
                    self.request,
                    "You didn't enter any search criteria!"
                )
                return redirect(reverse('shop'))
        return super(Shop, self).dispatch(request, *args, **kwargs)

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

        self.queryset = Product.objects.all().order_by('brand')

        if sort_by:
            rating_none = None
            self.sort = sort_by
            if sort_direction:
                self.direction = sort_direction
                if sort_direction == 'desc':
                    sort_by = f'-{sort_by}'
                    rating_none = 0

            if 'brand' in sort_by:
                sort_by = sort_by.replace('brand', 'lower_brand')
                self.queryset = self.queryset.annotate(
                    lower_brand=Lower('brand__friendly_name'))

            if 'rating' in sort_by:
                self.queryset = self.queryset.annotate(
                    review_count=Count('reviews')).annotate(
                    rating_sum=Sum('reviews__rating')).annotate(
                    rating=Coalesce(F('rating_sum') / F('review_count'),
                                    rating_none))

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

        if self.search_query:
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

            if product.brand.country:
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

            if product.flavour:
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


def product_detail(request, product_id):
    """
    A view to show individual Product model
    objects on product_detail.html
    """
    product = get_object_or_404(Product, pk=product_id)
    reviews = product.reviews.all()
    updating_product = request.session.get('updating_product', False)

    if request.method == 'POST':
        try:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.product = product
                review.rating = request.POST.get('rating')
                review.save()
                messages.success(
                    request,
                    'Your review has been successfully submitted')
                request.session['reviewing'] = True

                return HttpResponse(status=200)
            else:
                messages.error(
                    request,
                    ('Your review submission has failed. Please '
                     'ensure the form is valid.')
                )
                request.session['reviewing'] = True
                return HttpResponse(status=200)
        except Exception as e:
            messages.error(request, f'Error submitting review: {e}')
            return HttpResponse(status=500)
    else:
        form = ReviewForm()

    reviewing = request.session.get('reviewing', False)

    if request.user.is_anonymous:
        wishlist = None
    else:
        try:
            wishlist = UserWishlist.objects.get(user=request.user)
            if product in wishlist.product.all():
                wishlist = True
            else:
                wishlist = False
        except ObjectDoesNotExist:
            wishlist = False

    template = 'shop/product_detail.html'
    context = {
        'product': product,
        'wishlist': wishlist,
        'viewing_detail': True,
        'form': form,
        'range': range(10),
        'reviewing': reviewing,
        'reviews': reviews,
        'updating_product': updating_product,
    }

    return render(request, template, context)


@login_required
def delete_review(request, review_id):
    """
    A view to delete a review from a product
    """
    review = get_object_or_404(Review, pk=review_id)
    product = review.product
    request.session['updating_cart'] = False
    request.session['reviewing'] = True
    request.session['updating_product'] = False

    if not request.user.is_superuser and not request.user == review.user:
        messages.error(
            request,
            'Sorry, only review authors and shop '
            'admins can delete reviews.'
        )
        return redirect(reverse('home'))
        
    try:
        review.delete()
        messages.success(
            request,
            f'Deleted review from "{product.brand.friendly_name}: '
            f'{product.name}". '
        )
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, f'Error deleting review: {e}')
        return HttpResponse(status=500)


# CREDIT - Idea and basic structure of the add, edit and delete product
# functions came from Code Institue's walkthrough project 'Boutique Ado'
@login_required
def add_product(request):
    """
    A view to add a product to the shop
    """
    request.session['updating_cart'] = False
    request.session['reviewing'] = False
    request.session['updating_product'] = True

    if not request.user.is_superuser:
        messages.error(
            request,
            'Sorry, only shop admins can add '
            'a product.'
        )
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request,
                'Failed to add product. Please ensure the '
                'form is valid.'
            )
    else:
        form = ProductForm()

    template = 'shop/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """
    A view to edit a product in the shop
    """
    request.session['updating_cart'] = False
    request.session['reviewing'] = False
    request.session['updating_product'] = True

    if not request.user.is_superuser:
        messages.error(
            request,
            'Sorry, only shop admins can edit '
            'a product.'
        )
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request,
                'Failed to update product. Please ensure the '
                'form is valid.'
            )
    else:
        form = ProductForm(instance=product)
        messages.info(
            request,
            f'You are editing {product.brand.friendly_name}: '
            f'{product.name}'
        )

    template = 'shop/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """
    A view to delete a product from the shop
    """
    request.session['updating_cart'] = False
    request.session['reviewing'] = False
    request.session['updating_product'] = True
    previous_url = request.META.get('HTTP_REFERER')

    if not request.user.is_superuser:
        messages.error(
            request,
            'Sorry, only shop admins can delete '
            'a product.'
        )
        return redirect(reverse('home'))

    try:
        product = get_object_or_404(Product, pk=product_id)
        product.delete()
        messages.success(request, 'Product deleted!')
        if f'/shop/{product_id}/' in previous_url:
            return redirect(reverse('shop'))
        else:
            return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, f'Error deleting product: {e}')
        if f'/shop/{product_id}/' in previous_url:
            return redirect(reverse('shop'))
        else:
            return HttpResponse(status=500)
