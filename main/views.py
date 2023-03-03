from .models import Products, Category, ShortApplication, Recipe, FieldOfActivity
from rest_framework import generics, views, pagination, filters
from .serializers import ProductsSerializer, Categoryserializer, ShortApplicationSerializer, TranslationsSerializerBadVersion
from .serializers import ArticleSerializer, StaticInformationSerializer, TranslationSerializer, LangsSerializer, PartnersSerializer, ArticleDetailSerializer
from .serializers import FAQserializer, RecipeSerializer, ActivitySerializer
from admins.models import Articles, StaticInformation, Partners, Translations, Languages, FAQ
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .utils import search_func
# Create your views here.

# pagination
class BasePagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000


# articles list
class ArticlesList(generics.ListAPIView):
    queryset = Articles.objects.filter(active=True)
    serializer_class = ArticleSerializer
    pagination_class = BasePagination


# articles detail
class ArticlesDetail(generics.RetrieveAPIView):
    queryset = Articles.objects.filter(active=True)
    serializer_class = ArticleDetailSerializer
    lookup_field = 'slug'


# static information
class StaticInfView(views.APIView):
    def get(self, request, format=None):
        try:
            obj = StaticInformation.objects.get(id=1)
        except:
            obj = StaticInformation.objects.create()

        serializer = StaticInformationSerializer(obj, context={'request': request})

        return Response(serializer.data)


# translations
class TranslationsView(views.APIView):
    def get(self, request, fromat=None):
        translations = Translations.objects.all()
        serializer = TranslationSerializer(translations, context={'request': request})
        return Response(serializer.data)


# langs list
class LangsList(generics.ListAPIView):
    queryset = Languages.objects.filter(active=True)
    serializer_class = LangsSerializer
    pagination_class = BasePagination


# partners list
class PartnersList(generics.ListAPIView):
    queryset = Partners.objects.all()
    serializer_class = PartnersSerializer
    pagination_class = BasePagination


# category list
class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = Categoryserializer
    pagination_class = BasePagination


# category detail
class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = Categoryserializer


# products list
class ProductsList(generics.ListAPIView):
    serializer_class = ProductsSerializer
    pagination_class = BasePagination


    def get_queryset(self):
        queryset = Products.objects.filter(active=True)
        ctg_id = self.request.GET.get("category", '')

        if ctg_id != '':
            category_qs = Category.objects.all()
            category = get_object_or_404(category_qs, id=int(ctg_id))
            queryset = queryset.filter(category=category)

        return queryset


# product variant detail view
class ProductDetail(generics.RetrieveAPIView):
    queryset = Products.objects.filter(active=True)
    serializer_class = ProductsSerializer
    lookup_field = 'slug'


# top products view
class MainProductsView(generics.RetrieveAPIView):
    serializer_class = ProductsSerializer
    pagination_class = BasePagination

    def get_object(self):
        queryset = Products.objects.filter(active=True)
        return get_object_or_404(queryset, main=True)



# faq view
class FAQview(generics.ListAPIView):
    queryset = FAQ.objects.filter(active=True)
    serializer_class = FAQserializer
    pagination_class = BasePagination


# recipe serializer
class RecipeView(generics.ListAPIView):
    queryset = Recipe.objects.filter(active=True)
    serializer_class = RecipeSerializer
    pagination_class = BasePagination


# recipe detail
class RecipeDetail(generics.RetrieveAPIView):
    queryset = Recipe.objects.filter(active=True)
    serializer_class = RecipeSerializer
    lookup_field = 'slug'


# application add
class NewAppliction(generics.CreateAPIView):
    serializer_class = ShortApplicationSerializer
    queryset = ShortApplication.objects.all()

        

# activity list
class ActivitiesList(generics.ListAPIView):
    queryset = FieldOfActivity.objects.filter(active=True)
    serializer_class = ActivitySerializer


        
        




