# Generated by Django 3.2 on 2022-04-06 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20220405_1524'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='country',
        ),
        migrations.RemoveField(
            model_name='product',
            name='region',
        ),
        migrations.AddField(
            model_name='brand',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.country'),
        ),
        migrations.AddField(
            model_name='brand',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.region'),
        ),
    ]
