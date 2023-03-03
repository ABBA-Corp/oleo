from django.urls import path, include
from . import views


urlpatterns = [
    path('articles', views.ArticlesList.as_view()),
    path("articles/<slug:slug>", views.ArticlesDetail.as_view()),
    path("static_infos", views.StaticInfView.as_view()),
    path("translations", views.TranslationsView.as_view()),
    path('languages', views.LangsList.as_view()),
    path('partners', views.PartnersList.as_view()),
    path('categories', views.CategoryList.as_view()),
    path("categories/<int:pk>", views.CategoryDetailView.as_view()),
    path('products', views.ProductsList.as_view()),
    path('products/<slug:slug>', views.ProductDetail.as_view()),
    path("main_product", views.MainProductsView.as_view()),
    path("add_aplication", views.NewAppliction.as_view()),
    path('faq', views.FAQview.as_view()),
    path("recipe", views.RecipeView.as_view()),
    path("recipe/<slug:slug>",views.RecipeDetail.as_view()),
    path("activities", views.ActivitiesList.as_view())
]