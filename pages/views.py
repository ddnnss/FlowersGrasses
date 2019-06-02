from django.shortcuts import render
from items.models import Category

# Create your views here.
def index(request):
    all_category = Category.objects.all()
    return render(request, 'pages/index.html', locals())

