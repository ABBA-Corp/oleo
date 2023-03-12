from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator
from easy_thumbnails.fields import ThumbnailerImageField
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from autoslug import AutoSlugField
from admins.models import Languages
from django.utils.text import slugify
import string
import random
from admins.models import unique_slug_generator, json_field_validate
import cyrtranslit
from admins.models import MetaTags
# Create your models here.



# category
class Category(models.Model):
    name = models.JSONField('Name', validators=[json_field_validate])
    deckription = models.JSONField("Deckription", blank=True, null=True)
    icon = ThumbnailerImageField(upload_to='ctg_icons', blank=True, null=True)
    image = ThumbnailerImageField(upload_to='ctg_image', blank=True, null=True)
    cotalog = models.FileField('Cotalog for download', upload_to='cotalog_fiels', blank=True, null=True)
    active = models.BooleanField(default=True)



# products
class Products(models.Model):
    name = models.JSONField('Name', validators=[json_field_validate])
    subtitle = models.JSONField('Subtitle', blank=True, null=True)
    slug = models.SlugField('Slug', editable=False, unique=True, blank=True, null=True)
    type = models.JSONField("Type", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', blank=True, null=True)
    description = models.JSONField('Descr', blank=True, null=True)
    bb_date = models.JSONField('BB date', blank=True, null=True)
    price = models.FloatField('Price', validators=[MinValueValidator(1)])
    active = models.BooleanField('Active', default=True)
    meta = models.ForeignKey(MetaTags, on_delete=models.CASCADE, blank=True, null=True)
    top = models.BooleanField('Top', default=False)
    image = ThumbnailerImageField(upload_to='product_images', blank=True, null=True)
    main = models.BooleanField('Main product', default=False)

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            lng = Languages.objects.filter(active=True).filter(default=True).first()
            str = cyrtranslit.to_latin(self.name.get(lng.code, '')[:50])
            slug = slugify(str)
            self.slug = unique_slug_generator(self, slug)

        if self.main:
            for prod in Products.objects.exclude(id=self.id):
                prod.main = False
                prod.save()

        return super().save(*args, **kwargs)


# field of activity
class FieldOfActivity(models.Model):
    name = models.JSONField('Name', validators=[json_field_validate])
    active = models.BooleanField(default=True)


# short applications
class ShortApplication(models.Model):
    STATUS = [('На рассмотрении', "На рассмотрении"),
              ("Рассмотрено", "Рассмотрено"), ("Отклонено", "Отклонено")]

    full_name = models.CharField('Full name', max_length=255)
    nbm = models.CharField('Nbm', max_length=255)
    product = models.ForeignKey(Products, blank=True, null=True, on_delete=models.SET_NULL)
    activity = models.ForeignKey(FieldOfActivity, on_delete=models.SET_NULL, blank=True, null=True)
    comment = models.TextField('Comment', blank=True, null=True)
    status = models.CharField(
        'Status', default='На рассмотрении', max_length=255, choices=STATUS)


# recipe
class Recipe(models.Model):
    title = models.JSONField('Заголовок', validators=[json_field_validate])
    slug = models.SlugField('Slug', editable=False, unique=True)
    subtitle = models.JSONField('Пост заголовок')
    body = models.JSONField("Статья")
    video = models.URLField('Youtube url', blank=True, null=True)
    image = ThumbnailerImageField('Image', blank=True ,null=True)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            lng = Languages.objects.filter(
                active=True).filter(default=True).first()
            str = cyrtranslit.to_latin(self.title.get(lng.code, '')[:50])
            slug = slugify(str)
            self.slug = unique_slug_generator(self, slug)

        return super().save(*args, **kwargs)


