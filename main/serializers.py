from .models import Products, Category, ShortApplication, Recipe, FieldOfActivity
from admins.models import Languages
from rest_framework import serializers
from django.conf import settings
from django.core.files.storage import default_storage
import os
from easy_thumbnails.templatetags.thumbnail import thumbnail_url, get_thumbnailer
from admins.models import Articles, StaticInformation, Languages, Translations, MetaTags, Partners, FAQ


class ThumbnailSerializer(serializers.BaseSerializer):
    def __init__(self, alias, instance=None, **kwargs):
        super().__init__(instance, **kwargs)
        self.alias = alias

    def to_representation(self, instance):
        alias = settings.THUMBNAIL_ALIASES.get('').get(self.alias)
        if alias is None:
            return None

        size = alias.get('size')[0]
        url = None

        if instance:
            orig_url = instance.path.split('.')
            thb_url = '.'.join(orig_url) + f'.{size}x{size}_q85.{orig_url[-1]}'
            if default_storage.exists(thb_url):
                last_url = instance.url.split('.')
                url = '.'.join( last_url) + f'.{size}x{size}_q85.{last_url[-1]}'
            else:
                url = get_thumbnailer(instance)[self.alias].url

        if url == '' or url is None:
            return None

        request = self.context.get('request', None)
        if request is not None:
            return request.build_absolute_uri(url)

        return url


# format date
def get_format_date(date):
    m = str(date.month)
    if len(m) == 1:
        m = '0' + m

    d = str(date.day)
    if len(d) == 1:
        d = '0' + d

    return d + '.' + m + '.' + str(date.year)


# based model serializer
class BasedModelSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        data_dict = {}
        default_lang = Languages.objects.filter(default=True).first()
        lang = self.context.get('lang')
        fields = self.context.get("fields")
        image_fields = self.context.get("image_fields")
        for field in fields:
            if 'date' in str(field):
                try:
                    data_dict[field] = get_format_date(instance.get(field))
                except:
                    data_dict[field] = None
                continue

            try: 
                data = instance.get(field).get(lang)
                if data is None or data == '':
                    data = instance.get(field, {}).get(default_lang)
            except:
                data_dict[field] = instance.get(field, None)

    
        for image in image_fields:
            data_dict[image] = ThumbnailSerializer(instance=instance.get(image), alias='prod_photo', context={'request': self.context.get("request")}).data


        return data_dict


# field lang serializer
class JsonFieldSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        language = self.context['request'].headers.get('Language')
        default_lang = Languages.objects.filter(default=True).first().code

        if not language:
            language = default_lang
        
        data = instance.get(language)
        
        if data is None or data == '':
            data = instance.get(default_lang)

        return data


# meta serializer
class MetaFieldSerializer(serializers.ModelSerializer):
    meta_keys = JsonFieldSerializer()
    meta_deck = JsonFieldSerializer()

    class Meta:
        model = MetaTags
        exclude = ['id']



# category serializer
class Categoryserializer(serializers.ModelSerializer):
    name = JsonFieldSerializer()
    deckription = JsonFieldSerializer()
    icon = ThumbnailSerializer(alias='ten')
    image = ThumbnailSerializer(alias='ten')

    class Meta:
        model = Category
        fields = '__all__'


# category simple serializer
class CategorySimpleSerializer(serializers.ModelSerializer):
    name = JsonFieldSerializer()

    class Meta:
        model = Category
        fields = ['name', 'id']



# product serializer
class ProductsSerializer(serializers.ModelSerializer):
    name = JsonFieldSerializer()
    subtitle = JsonFieldSerializer()
    type = JsonFieldSerializer()
    bb_date = JsonFieldSerializer()
    category = CategorySimpleSerializer()
    description = JsonFieldSerializer()
    meta = MetaFieldSerializer()
    image = ThumbnailSerializer(alias='biiiig')

    class Meta:
        model = Products
        fields = '__all__'



# articles
class ArticleSerializer(serializers.ModelSerializer):
    title = JsonFieldSerializer()
    subtitle = JsonFieldSerializer()
    body = JsonFieldSerializer()
    created_date = serializers.DateField(format="%d.%m.%Y")
    image = ThumbnailSerializer(alias='prod_photo')
    author = serializers.ReadOnlyField(source='author.username')
    meta = MetaFieldSerializer()

    class Meta:
        model = Articles
        fields = '__all__'

    
# article detail serializer
class ArticleDetailSerializer(serializers.ModelSerializer):
    title = JsonFieldSerializer()
    subtitle = JsonFieldSerializer()
    body = JsonFieldSerializer()
    created_date = serializers.DateField(format="%d.%m.%Y")
    image = ThumbnailSerializer(alias='original')
    meta = MetaFieldSerializer()

    class Meta:
        model = Articles
        fields = '__all__'


# static information
class StaticInformationSerializer(serializers.ModelSerializer):
    title = JsonFieldSerializer()
    subtitle = JsonFieldSerializer()
    deskription = JsonFieldSerializer()
    about_us = JsonFieldSerializer()
    adres = JsonFieldSerializer()
    work_time = JsonFieldSerializer()
    logo_first = ThumbnailSerializer(alias='prod_photo')
    logo_second = ThumbnailSerializer(alias='prod_photo')

    class Meta:
        model = StaticInformation
        exclude = ['id']


# translation serializer
class TranslationSerializer(serializers.Serializer):
    def to_representation(self, instance):
        data = {}

        for item in instance:
            val = JsonFieldSerializer(item.value, context={'request': self.context.get('request')}).data
            key = str(item.group.sub_text) + '.' + str(item.key)
            data[key] = val

        return data


# class TransaltionForDostonaka
class TranslationsSerializerBadVersion(serializers.Serializer): 
    def to_representation(self, instance):
        data = {}
        languages = Languages.objects.filter(active=True)
        def_lang = languages.filter(default=True).first()
        
        for lang in languages:
            data[lang.code] = {}
            new_data = {}
            for item in instance:
                val = JsonFieldSerializer(item.value, context={'request': self.context.get('request')}).data
                key = str(item.key)
                new_data[key] = val

            data[lang.code] = new_data

        return data


# langs serializer
class LangsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Languages
        fields = '__all__'


# parnters serializer
class PartnersSerializer(serializers.ModelSerializer):
    name = JsonFieldSerializer()
    deckription = JsonFieldSerializer()
    image = ThumbnailSerializer(alias='product_img')

    class Meta:
        model = Partners
        fields = '__all__'



# short apl serializer
class ShortApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortApplication
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        product_serializer = ProductsSerializer(instance.product, context={'request': self.context.get("request")})
        data['product'] = product_serializer.data

        return data



# FAQ serializer
class FAQserializer(serializers.ModelSerializer):
    question = JsonFieldSerializer()
    answer = JsonFieldSerializer()

    class Meta:
        model = FAQ
        exclude = ['active']



# recipe serializer
class RecipeSerializer(serializers.ModelSerializer):
    title = JsonFieldSerializer()
    subtitle = JsonFieldSerializer()
    body = JsonFieldSerializer()
    image = ThumbnailSerializer(alias='recipe_img')

    class Meta:
        model = Recipe
        exclude = ['active']


# activity serializer
class ActivitySerializer(serializers.ModelSerializer):
    name = JsonFieldSerializer()

    class Meta:
        model = FieldOfActivity
        fields = '__all__'