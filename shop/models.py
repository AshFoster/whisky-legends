from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Type(models.Model):
    name = models.SlugField(max_length=254, unique=True)
    friendly_name = models.CharField(max_length=254, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name)

    def get_friendly_name(self):
        return self.friendly_name

    def save(self, *args, **kwargs):
        self.name = slugify(self.friendly_name)
        super(Type, self).save(*args, **kwargs)


class Brand(models.Model):
    name = models.SlugField(max_length=254, unique=True)
    friendly_name = models.CharField(max_length=254, unique=True)
    country = models.ForeignKey(
        'Country',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    region = models.ForeignKey(
        'Region',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name)

    def get_friendly_name(self):
        return self.friendly_name

    def save(self, *args, **kwargs):
        self.name = slugify(self.friendly_name)
        super(Brand, self).save(*args, **kwargs)


class Country(models.Model):
    name = models.SlugField(max_length=254, unique=True)
    friendly_name = models.CharField(max_length=254, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Countries'

    def __str__(self):
        return str(self.name)

    def get_friendly_name(self):
        return self.friendly_name

    def save(self, *args, **kwargs):
        self.name = slugify(self.friendly_name)
        super(Country, self).save(*args, **kwargs)


class Region(models.Model):
    name = models.SlugField(max_length=254, unique=True)
    friendly_name = models.CharField(max_length=254, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name)

    def get_friendly_name(self):
        return self.friendly_name

    def save(self, *args, **kwargs):
        self.name = slugify(self.friendly_name)
        super(Region, self).save(*args, **kwargs)


class Flavour(models.Model):
    name = models.SlugField(max_length=254, unique=True)
    friendly_name = models.CharField(max_length=254, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name)

    def get_friendly_name(self):
        return self.friendly_name

    def save(self, *args, **kwargs):
        self.name = slugify(self.friendly_name)
        super(Flavour, self).save(*args, **kwargs)


class Product(models.Model):
    type = models.ForeignKey(
        'Type',
        on_delete=models.CASCADE
    )
    brand = models.ForeignKey(
        'Brand',
        on_delete=models.CASCADE
    )
    flavour = models.ForeignKey(
        'Flavour',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    abv = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True)
    volume = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True)
    age = models.IntegerField(null=True, blank=True)
    rated = models.ManyToManyField(
        User,
        related_name='product_rated',
        blank=True
    )
    wishlist = models.ManyToManyField(
        User,
        related_name='product_wishlist',
        blank=True
    )
    rating_total = models.IntegerField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def calc_rating(self):
        if self.rating_total and self.rated.count() != 0:
            print(self.rated.count())
            return self.rating_total/self.rated.count()
