"""Views to manage food_substitute"""
from collections import Counter

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User

from .models import Category, Products, Favorites


def welcome(request):
    """Display welcome page"""
    return render(request, "food_substitute/welcome.html")


def detail(request, code):
    """Display detail view of products"""
    product = get_object_or_404(Products, code=code)

    context = {"product": product}
    return render(request, "food_substitute/detail.html", context)


def disclaimer(request):
    """Display disclaimer page"""
    return render(request, "food_substitute/disclaimer.html")


def search(request):
    """Search products according to user's queries"""
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
            """Select categories above 20% occurences"""
            categories_sorted = Counter(categories).most_common()
            categories_most = []
            for elem in categories_sorted:
                if elem[1] / len(categories) > 0.2:
                    categories_most.append(elem[0])
            prods = []
            for categ in categories_most:
                products = Products.objects.filter(category__name=categ.name)
                prods.append(products)
            for prod in prods:
                for productos in prod:
                    if (
                        productos.nutrition_grades != ""
                        and productos.nutrition_grades < product.nutrition_grades
                    ):
                        better_prods.append(productos)
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
            product = None
            prods = None
            better_p = None

        context = {
            "product": product,
            "better_prods": better_p,
            "title_prod_missing": f"Il n'y a pas de produits '{query}' dans"
            " la base de données",
            "better": better,
            "paginate": True,
            "query": query,
        }

    return render(request, "food_substitute/category.html", context)


def save(request, produc, substitut):
    """Save users' substitutes"""
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        product = Products.objects.get(code=produc)
        substitute = Products.objects.get(code=substitut)
        duplicates = False
        recorded = Favorites.objects.filter(users=user)
        favorite_recorded = []
        for record in recorded:
            rec = (
                Products.objects.get(id=record.products_id),
                Products.objects.get(id=record.substitute_id),
            )
            favorite_recorded.append(rec)
        if (
            len(
                Favorites.objects.filter(
                    users=user, products=product, substitute=substitute
                )
            )
            > 0
        ):
            duplicates = True
        else:
            record = Favorites(users=user, products=product, substitute=substitute)
            record.save()
        recording = True
        context = {
            "recording": recording,
            "user": user,
            "product": product,
            "substitute": substitute,
            "duplicates": duplicates,
            "favorite_recorded": favorite_recorded,
        }
        return render(request, "food_substitute/favorites.html", context)
    return redirect("login")


def favorites(request):
    """Display user's recorded substitutes"""
    user_id = request.user.id
    user = get_object_or_404(User, id=user_id)
    recorded = Favorites.objects.filter(users=user)
    favorite_recorded = []
    for record in recorded:
        rec = (
            Products.objects.get(id=record.products_id),
            Products.objects.get(id=record.substitute_id),
        )
        favorite_recorded.append(rec)

    recording = False
    context = {
        "recording": recording,
        "favorite_recorded": favorite_recorded,
    }

    return render(request, "food_substitute/favorites.html", context)
