# Generated by Django 4.1 on 2023-02-22 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_remove_products_manufacturer'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='main_products',
            field=models.BooleanField(default=False, verbose_name='Main product'),
        ),
    ]
