from django.shortcuts import render
#~ from django.views import generic
from .models import Category, Products
from .API import product_data, search_data
from .forms import CategoryForm

# Create your views here.

def welcome(request):
    return render(request, "food_substitute/welcome.html")

#~ class DetailView(generic.DetailView):
    #~ model=Products
    #~ template_name='food_substitute/detail.html'

def detail(request, code):
    context=product_data(code)
    return render(request, 'food_substitute/detail.html', context)
    
def disclaimer(request):
    return render(request, "food_substitute/disclaimer.html")

#~ def search(request):
    #~ form=CategoryForm()
    #~ return render(request, "food_substitute/category.html", {'form': form})

def search(request):
    query = request.GET.get('query')
    if not query:
        context={'message':'Veuillez entrez une catégorie'}
    else:
        prod_name=search_data(query)
        context={'name': prod_name}

    #~ if not albums.exists():
        #~ albums = Album.objects.filter(artists__name__icontains=query)
    #~ title = "Résultats pour la requête %s"%query
    #~ context = {
        #~ 'albums': albums,
        #~ 'title': title
    #~ }
    return render(request, "food_substitute/category.html", context)
