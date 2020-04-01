from django.shortcuts import render
from django.views import generic
from .models import Category, Products
from .API import product_data

# Create your views here.

def welcome(request):
    return render(request, "food_substitute/welcome.html")

#~ class DetailView(generic.DetailView):
    #~ model=Products
    #~ template_name='food_substitute/detail.html'

def detail(request, code):
    context=product_data(code)
    print(context)
    return render(request, 'food_substitute/detail.html', context)
    
def disclaimer(request):
    return render(request, "food_substitute/disclaimer.html")
