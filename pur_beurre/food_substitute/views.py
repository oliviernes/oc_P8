from django.shortcuts import render
from django.views import generic
from .models import Category, Products

# Create your views here.


def welcome(request):
    return render(request, "food_substitute/welcome.html")

class DetailView(generic.DetailView):
    model=Products
    template_name='food_substitute/detail.html'

def disclaimer(request):
    return render(request, "food_substitute/disclaimer.html")
