from django.test import Client

from pytest import mark

from food_substitute.models import Products

####################
###  search view ###
####################

@mark.django_db
def test_search_missing_prod():

    c = Client()
    response = c.get("/search/?query=Nutella")

    assert (
        response.context["title_prod_missing"]
        == "Il n'y a pas de produits 'Nutella' dans la base de données"
    )


@mark.django_db
def test_search_no_query():

    c = Client()
    response = c.get("/search/?query=")

    assert response.context["message"] == "Veuillez entrez un produit"


@mark.django_db
def test_search_product():

    prod = Products.objects.create(name="Nutella", code="1")

    c = Client()
    response = c.get("/search/?query=Nutella")
    prod = response.context["product"]

    assert prod.name == "Nutella"


@mark.django_db
def test_search_partial_query():

    prod = Products.objects.create(name="Nutella", code="1")

    c = Client()
    response = c.get("/search/?query=Nutel")
    prod = response.context["product"]

    assert prod.name == "Nutella"

###################
### detail view ###
###################

@mark.django_db
def test_detail_product():

    prod = Products.objects.create(name="Nutella", code="123456789")

    c=Client()
    response = c.get("/product/123456789")
    prod = response.context["product"]

    assert prod.name == "Nutella"
