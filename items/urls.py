from django.urls import path
from . import views

urlpatterns = [

    path('item/<item_slug>', views.product, name='product'),
    path('category/<category_slug>', views.cat, name='cat'),
    path('collection/<collection_slug>', views.collection, name='collection'),
    path('search/', views.search, name='search'),




]
