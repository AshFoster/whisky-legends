# Generated by Django 3.2 on 2022-05-04 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_remove_product_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='wishlist',
        ),
    ]
