from django.test import Client
from django.contrib.auth.models import User

from pytest import mark

from food_substitute.models import Products

####################
###  search view ###
####################

import pdb

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

@mark.django_db
def test_login_valid_user():
    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    c = Client()

    response = c.login(username= 'john', password= 'johnpassword')

    response2 = c.post("/login/", {'username': 'john', 'password': 'johnpassword'})

    assert response == True
    assert response2.url == "/my_account/"
    assert response2.status_code == 302

@mark.django_db
def test_login_wrong_user():

    c = Client()

    response = c.post("/login/", {'username': 'tartampion', 'password': 'johnpassword'})

    assert response.status_code == 200
    assert response.templates[0].name == "registration/login.html"
    assert response.templates[1].name == "food_substitute/base.html"

@mark.django_db
def test_login_wrong_password():

    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    c = Client()

    response = c.login(username= 'john', password= 'wrongpassword')

    response2 = c.post("/login/", {'username': 'john', 'password': 'wrongpassword'})

    assert response == False
    assert response2.status_code == 200
    assert response2.templates[0].name == "registration/login.html"
    assert response2.templates[1].name == "food_substitute/base.html"

@mark.django_db
def test_login_no_user_recorded():

    c = Client()

    response = c.login(username= 'john', password= 'johnpassword')

    assert response == False

####################
### signup view ####
####################


def test_signup():

    c = Client()
    response = c.get("/signup/")

    assert response.status_code == 200
    assert response.templates[0].name == "registration/signup.html"
    assert response.templates[1].name == "food_substitute/base.html"

@mark.django_db
def test_signup_user():

    c = Client()

    response = c.post("/signup/", {
                                    'username': 'Mell1', 
                                    'first_name': 'Mell', 
                                    'last_name': 'MAMAMA', 
                                    'email': 'mell6@gmail.com', 
                                    'password1': 'monsupermdp1234', 
                                    'password2': 'monsupermdp1234', 
                                })

    assert response.url == "/my_account/"
    assert response.status_code == 302

@mark.django_db
def test_signup_user_incorrect_data():

    c = Client()

    response = c.post("/signup/", {
                                    'username': '', 
                                    'first_name': 'Mell', 
                                    'last_name': '', 
                                    'email': 'mell6gmail.com', 
                                    'password1': 'dd', 
                                    'password2': 'aa', 
                                })

    assert response.status_code == 200
    assert response.templates[0].name == "registration/signup.html"
    assert response.templates[1].name == "food_substitute/base.html"

@mark.django_db
def test_signup_user_email_already_used():

    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    c = Client()

    response = c.post("/signup/", {
                                    'username': 'Mell1', 
                                    'first_name': 'Mell', 
                                    'last_name': 'MAMAMA', 
                                    'email': 'lennon@thebeatles.com', 
                                    'password1': 'monsupermdp1234', 
                                    'password2': 'monsupermdp1234', 
                                })

    assert response.status_code == 200
    assert response.templates[0].name == "registration/signup.html"
    assert response.templates[1].name == "food_substitute/base.html"
