from django.shortcuts import render
from store.models import Product


def home(request):
    beverages = Product.objects.all().filter(is_available=True).order_by('id')
    context = {
        'beverages': beverages,
    }
    
    return render(request, 'home.html', context)