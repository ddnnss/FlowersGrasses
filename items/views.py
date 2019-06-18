from django.shortcuts import render
from .models import *

def product(request,item_slug):
    item = Item.objects.get(name_slug=item_slug)

    return render(request, 'pages/item.html', locals())

def cat(request,category_slug):
    category = Category.objects.get(name_slug=category_slug)
    filters = Filter.objects.filter(category=category)
    all_items = Item.objects.filter(category=category)
    return render(request, 'pages/category.html', locals())


def collection(request,collection_slug):
    collection = Collection.objects.get(name_slug=collection_slug)
    all_items = Item.objects.filter(collection=collection)
    return render(request, 'pages/collection.html', locals())