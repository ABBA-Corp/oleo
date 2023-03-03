from django.contrib import admin
from .models import Products, Category, Recipe, ShortApplication
# Register your models here.


admin.site.register(Products)
admin.site.register(Category)
admin.site.register(Recipe)
admin.site.register(ShortApplication)