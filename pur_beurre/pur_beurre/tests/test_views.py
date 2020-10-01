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
    assert response.status_code == 200
    assert response.templates[0].name == "food_substitute/category.html"
    assert response.templates[1].name == "food_substitute/base.html"



def test_search_no_query():

    c = Client()
    response = c.get("/search/?query=")

    assert response.context["message"] == "Veuillez entrez un produit"
    assert response.status_code == 200
    assert response.templates[0].name == "food_substitute/category.html"
    assert response.templates[1].name == "food_substitute/base.html"


@mark.django_db
def test_search_product():

    prod = Products.objects.create(name="Nutella", code="1")
    c = Client()
    response = c.get("/search/?query=Nutella")
    prod = response.context["product"]

    assert prod.name == "Nutella"
    assert response.status_code == 200
    assert response.templates[0].name == "food_substitute/category.html"
    assert response.templates[1].name == "food_substitute/base.html"


@mark.django_db
def test_search_partial_query():

    prod = Products.objects.create(name="Nutella", code="1")

    c = Client()
    response = c.get("/search/?query=Nutel")
    prod = response.context["product"]

    assert prod.name == "Nutella"
    assert response.status_code == 200
    assert response.templates[0].name == "food_substitute/category.html"
    assert response.templates[1].name == "food_substitute/base.html"


###################
### detail view ###
###################


@mark.django_db
def test_detail_product():

    prod = Products.objects.create(name="Nutella", code="123456789")

    c = Client()
    response = c.get("/product/123456789")
    prod = response.context["product"]

    assert prod.name == "Nutella"
    assert response.status_code == 200
    assert response.templates[0].name == "food_substitute/detail.html"
    assert response.templates[1].name == "food_substitute/base.html"

####################
### welcome view ###
####################


def test_welcome():

    c = Client()
    response = c.get("/")

    assert response.status_code == 200
    assert response.templates[0].name == "food_substitute/welcome.html"
    assert response.templates[1].name == "food_substitute/base.html"

####################
### login view #####
####################


def test_login():

    c = Client()
    response = c.get("/login/")

    assert response.status_code == 200
    assert response.templates[0].name == "registration/login.html"
    assert response.templates[1].name == "food_substitute/base.html"



####################
### signup view ####
####################


def test_signup():

    c = Client()
    response = c.get("/signup/")

    assert response.status_code == 200
    assert response.templates[0].name == "registration/signup.html"
    assert response.templates[1].name == "food_substitute/base.html"

