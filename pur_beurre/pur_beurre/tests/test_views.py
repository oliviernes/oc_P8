from django.test import Client
from django.contrib.auth.models import User

from pytest import mark

from food_substitute.models import Products

####################
###  search view ###
####################

import pdb

class TestSearch:

    client = Client()

    @mark.django_db
    def test_search_missing_prod(self):

        response = self.client.get("/search/?query=Nutella")

        assert (
            response.context["title_prod_missing"]
            == "Il n'y a pas de produits 'Nutella' dans la base de données"
        )
        assert response.status_code == 200
        assert response.templates[0].name == "food_substitute/category.html"
        assert response.templates[1].name == "food_substitute/base.html"
        assert response.context['query'] == "Nutella"

    def test_search_no_query(self):

        response = self.client.get("/search/?query=")

        assert response.context["message"] == "Veuillez entrez un produit"
        assert response.status_code == 200
        assert response.templates[0].name == "food_substitute/category.html"
        assert response.templates[1].name == "food_substitute/base.html"


    @mark.django_db
    def test_search_product(self):

        prod = Products.objects.create(name="Nutella", code="1")
        response = self.client.get("/search/?query=Nutella")
        prod = response.context["product"]

        assert prod.name == "Nutella"
        assert response.status_code == 200
        assert response.templates[0].name == "food_substitute/category.html"
        assert response.templates[1].name == "food_substitute/base.html"


    @mark.django_db
    def test_search_partial_query(self):

        prod = Products.objects.create(name="Nutella", code="1")

        response = self.client.get("/search/?query=Nutel")
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

    client = Client()
    response = client.get("/product/123456789")
    prod = response.context["product"]

    assert prod.name == "Nutella"
    assert response.status_code == 200
    assert response.templates[0].name == "food_substitute/detail.html"
    assert response.templates[1].name == "food_substitute/base.html"

####################
### welcome view ###
####################


def test_welcome():

    client = Client()
    response = client.get("/")

    assert response.status_code == 200
    assert response.templates[0].name == "food_substitute/welcome.html"
    assert response.templates[1].name == "food_substitute/base.html"

####################
### login view #####
####################

class TestLogin:

    client = Client()

    def test_login(self):

        response = self.client.get("/login/")

        assert response.status_code == 200
        assert response.templates[0].name == "registration/login.html"
        assert response.templates[1].name == "food_substitute/base.html"

    @mark.django_db
    def test_login_valid_user(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

        response = self.client.login(username= 'lennon@thebeatles.com', password= 'johnpassword')

        response2 = self.client.post("/login/", {'username': 'lennon@thebeatles.com', 'password': 'johnpassword'})

        assert response == True
        assert response2.url == "/my_account/"
        assert response2.status_code == 302

    @mark.django_db
    def test_login_wrong_user(self):

        response = self.client.post("/login/", {'username': 'tartampion', 'password': 'johnpassword'})

        assert response.status_code == 200
        assert response.templates[0].name == "registration/login.html"
        assert response.templates[1].name == "food_substitute/base.html"

    @mark.django_db
    def test_login_wrong_password(self):

        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

        response = self.client.login(username= 'lennon@thebeatles.com', password= 'wrongpassword')

        response2 = self.client.post("/login/", {'username': 'lennon@thebeatles.com', 'password': 'wrongpassword'})

        assert response == False
        assert response2.status_code == 200
        assert response2.templates[0].name == "registration/login.html"
        assert response2.templates[1].name == "food_substitute/base.html"

    @mark.django_db
    def test_login_no_user_recorded(self):

        response = self.client.login(username= 'lennon@thebeatles.com', password= 'johnpassword')

        assert response == False

####################
### signup view ####
####################

class TestSignup:

    client = Client()
    
    def test_signup(self):


        response = self.client.get("/signup/")

        assert response.status_code == 200
        assert response.templates[0].name == "registration/signup.html"
        assert response.templates[1].name == "food_substitute/base.html"

    @mark.django_db
    def test_signup_right_infos(self):

        response = self.client.post("/signup/", {
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
    def test_signup_user_incorrect_data(self):

        response = self.client.post("/signup/", {
                                        'username': '',
                                        'first_name': '',
                                        'last_name': '',
                                        'email': 'pimail.com',
                                        'password1': 'aa',
                                        'password2': 'bb',
                                        })

        assert response.status_code == 200
        assert response.templates[0].name == "registration/signup.html"
        assert response.templates[1].name == "food_substitute/base.html"

    @mark.django_db
    def test_signup_user_email_already_used(self):

        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

        response = self.client.post("/signup/", {
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

####################
### save view   ####
####################

class TestSave:

    client = Client()

    @mark.django_db
    def test_save_user_connected(self):

        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        prod = Products.objects.create(name="Prince goût chocolat", code="7622210449283")
        prod2 = Products.objects.create(name="Véritable petit beurre", code="7622210988034")

        response = self.client.login(username= 'lennon@thebeatles.com', password= 'johnpassword')

        response2 = self.client.post("/save/7622210988034/7622210449283")

        assert response == True
        assert response2.status_code == 200
        assert response2.templates[0].name == "food_substitute/favorites.html"

    @mark.django_db
    def test_save_user_not_connected(self):

        prod = Products.objects.create(name="Prince goût chocolat", code="7622210449283")
        prod2 = Products.objects.create(name="Véritable petit beurre", code="7622210988034")

        response = self.client.post("/save/7622210988034/7622210449283")

        assert response.status_code == 302
        assert response.url == "/login/"

####################
### favorites view #
####################

@mark.django_db
def test_favorites():

    client = Client()

    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    response = client.login(username= 'lennon@thebeatles.com', password= 'johnpassword')

    response2 = client.get("/favorites/")

    assert response == True
    assert response2.status_code == 200
    assert response2.templates[0].name == "food_substitute/favorites.html"
