# Generated by Django 4.1 on 2023-02-20 10:43

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import easy_thumbnails.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admins', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.JSONField(blank=True, null=True, verbose_name='Name')),
                ('deckription', models.JSONField(blank=True, null=True, verbose_name='Deckription')),
                ('icon', easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to='ctg_icons')),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to='ctg_image')),
                ('cotalog', models.FileField(blank=True, null=True, upload_to='cotalog_fiels', verbose_name='Cotalog for download')),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.JSONField(blank=True, null=True, verbose_name='Name')),
                ('subtile', models.JSONField(blank=True, null=True, verbose_name='Subtitle')),
                ('slug', models.SlugField(blank=True, editable=False, null=True, unique=True, verbose_name='Slug')),
                ('type', models.JSONField(blank=True, null=True, verbose_name='Type')),
                ('manufacturer', models.JSONField(blank=True, null=True, verbose_name='Manuf')),
                ('description', models.JSONField(blank=True, null=True, verbose_name='Descr')),
                ('bb_date', models.JSONField(blank=True, null=True, verbose_name='BB date')),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Price')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('top', models.BooleanField(default=False, verbose_name='Top')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='main.category')),
                ('meta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admins.metatags')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.JSONField(verbose_name='??????????????????')),
                ('slug', models.SlugField(editable=False, unique=True, verbose_name='Slug')),
                ('subtitle', models.JSONField(verbose_name='???????? ??????????????????')),
                ('body', models.JSONField(verbose_name='????????????')),
                ('video', models.FileField(upload_to='', verbose_name='Video')),
            ],
        ),
        migrations.CreateModel(
            name='ShortApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255, verbose_name='Full name')),
                ('nbm', models.CharField(max_length=255, verbose_name='Nbm')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Comment')),
                ('status', models.CharField(choices=[('???? ????????????????????????', '???? ????????????????????????'), ('??????????????????????', '??????????????????????'), ('??????????????????', '??????????????????')], default='???? ????????????????????????', max_length=255, verbose_name='Status')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.products')),
            ],
        ),
    ]
