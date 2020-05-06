from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Category, Products


def welcome(request):
    return render(request, "food_substitute/welcome.html")


def detail(request, code):
    product = Products.objects.get(code=code)

    context = {"product": product}
    return render(request, "food_substitute/detail.html", context)


def disclaimer(request):
    return render(request, "food_substitute/disclaimer.html")


def search(request):
    query = request.GET.get("query")
    if not query:
        product = None
        context = {"product": product, "message": "Veuillez entrez un produit"}
    else:
        product = Products.objects.filter(name__contains=query)
        better_prods = []
        better = False
        if len(product) > 0:
            """Select the first product if several products of the \
same name are in the database"""
            product = product[0]
            """Select products belongings to the different categories \
of the product selected"""
            categories = Category.objects.filter(products__name__contains=query)
            prods = []
            for categ in categories:
                products = Products.objects.filter(category__name=categ.name)
                prods.append(products)
            for prod in prods:
                for p in prod:
                    if (
                        p.nutrition_grades != ""
                        and p.nutrition_grades < product.nutrition_grades
                    ):
                        better_prods.append(p)
            paginator = Paginator(better_prods, 9)
            page = request.GET.get("page")
            try:
                better_p = paginator.page(page)
            except PageNotAnInteger:
                better_p = paginator.page(1)
            except EmptyPage:
                better_p = paginator.page(paginator.num_pages)
            if len(better_prods) > 0:
                better = True
            else:
                better = False
        else:
            product = None
            prods = None
            better_p = None

        context = {
            "product": product,
            "better_prods": better_p,
            "title_prod_missing": f"Il n'y a pas de produits '{query}' dans la base de données",
            "better": better,
            "paginate": True,
            "query": query,
        }

    return render(request, "food_substitute/category.html", context)
