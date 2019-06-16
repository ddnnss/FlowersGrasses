from django.shortcuts import render
from items.models import Category,Collection

# Create your views here.
def index(request):
    all_category = Category.objects.all()
    all_collections = Collection.objects.all()
    return render(request, 'pages/index.html', locals())

