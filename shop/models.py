from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Type(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name)

    def get_friendly_name(self):
        return self.friendly_name


class Brand(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
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


class Country(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Countries'

    def __str__(self):
        return str(self.name)

    def get_friendly_name(self):
        return self.friendly_name


class Region(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name)

    def get_friendly_name(self):
        return self.friendly_name


class Flavour(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name)

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    type = models.ForeignKey(
        'Type',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    brand = models.ForeignKey(
        'Brand',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
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
    rating = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def calc_rating(self):
        self.rating = self.rating_total/self.rated.count()
