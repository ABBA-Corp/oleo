# Generated by Django 4.1 on 2023-02-20 13:34

from django.db import migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_recipe_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to='product_images'),
        ),
    ]
