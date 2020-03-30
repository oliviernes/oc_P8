from django.shortcuts import render

# Create your views here.



class DetailView(generic.DetailView):
    model=Products
    template_name='food_substitute/detail.html'

def disclaimer(request):
    return render(request, "food_substitute/disclaimer.html")
