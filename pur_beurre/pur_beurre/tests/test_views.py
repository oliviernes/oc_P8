from django.test import Client
from django.contrib.auth.models import User

from pytest import mark

from food_substitute.models import Products, Category, Favorites

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
    def test_search_no_better_product(self):

        cat = Category.objects.create(name="pâtes à tartiner au chocolat")
        prod = Products.objects.create(name="Nutella", code="1", nutrition_grades="e")
        other_prod = Products.objects.create(name="Pâte à tartiner lambda", code="2", nutrition_grades="e")
        prod.category.add(Category.objects.get(name=cat.name))
        prod.save()
        other_prod.category.add(Category.objects.get(name=cat.name))
        other_prod.save()

        response = self.client.get("/search/?query=Nutella")
        product = response.context["product"]

        assert product.name == "Nutella"
        assert response.status_code == 200
        assert response.templates[0].name == "food_substitute/category.html"
        assert response.templates[1].name == "food_substitute/base.html"
        assert response.context['paginate'] == True
        assert response.context['better'] == False

    @mark.django_db
    def test_search_better_product(self):

        cat = Category.objects.create(name="pâtes à tartiner au chocolat")
        prod = Products.objects.create(name="Nutella", code="1", nutrition_grades="e")
        better_prod = Products.objects.create(name="Pâte à tartiner", code="2", nutrition_grades="d")
        prod.category.add(Category.objects.get(name=cat.name))
        prod.save()
        better_prod.category.add(Category.objects.get(name=cat.name))
        better_prod.save()

        response = self.client.get("/search/?query=Nutella")
        product = response.context["product"]

        assert product.name == "Nutella"
        assert response.status_code == 200
        assert response.templates[0].name == "food_substitute/category.html"
        assert response.templates[1].name == "food_substitute/base.html"
        assert response.context['paginate'] == True
        assert response.context['better'] == True
        assert response.context['better_prods'][0].name == "Pâte à tartiner"

    @mark.django_db
    def test_search_partial_query(self):

        prod = Products.objects.create(name="Nutella", code="1")

        response = self.client.get("/search/?query=Nutel")
        product = response.context["product"]

        assert product.name == "Nutella"
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
    product = response.context["product"]

    assert product.name == "Nutella"
    assert response.status_code == 200
    assert response.templates[0].name == "food_substitute/detail.html"
    assert response.templates[1].name == "food_substitute/base.html"

@mark.django_db
def test_404_detail_product():

    client = Client()
    response = client.get("/product/123456789")

    assert response.status_code == 404

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

        response_login = self.client.login(username= 'lennon@thebeatles.com', password= 'johnpassword')

        response_post = self.client.post("/login/", {'username': 'lennon@thebeatles.com', 'password': 'johnpassword'})

        assert response_login == True
        assert response_post.url == "/my_account/"
        assert response_post.status_code == 302

    @mark.django_db
    def test_login_wrong_user(self):

        response = self.client.post("/login/", {'username': 'tartampion', 'password': 'johnpassword'})

        assert response.status_code == 200
        assert response.templates[0].name == "registration/login.html"
        assert response.templates[1].name == "food_substitute/base.html"

    @mark.django_db
    def test_login_wrong_password(self):

        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

        response_login = self.client.login(username= 'lennon@thebeatles.com', password= 'wrongpassword')

        response_post = self.client.post("/login/", {'username': 'lennon@thebeatles.com', 'password': 'wrongpassword'})

        assert response_login == False
        assert response_post.status_code == 200
        assert response_post.templates[0].name == "registration/login.html"
        assert response_post.templates[1].name == "food_substitute/base.html"

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
    def test_save_user_connected_and_favorite_already_recorded(self):

        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        subs = Products.objects.create(name="Prince goût chocolat", code="7622210449283")
        prod = Products.objects.create(name="Véritable petit beurre", code="7622210988034")

        fav = Favorites.objects.create(
                                        users = user,
                                        products = prod,
                                        substitute = subs,
                                        )

        response_login = self.client.login(username= 'lennon@thebeatles.com', password= 'johnpassword')

        response_post = self.client.post("/save/7622210988034/7622210449283")

        assert response_login == True
        assert response_post.status_code == 200
        assert response_post.templates[0].name == "food_substitute/favorites.html"
        assert response_post.context["recording"] == True
        assert response_post.context["duplicates"] == True
        assert response_post.context["user"] == user

    @mark.django_db
    def test_save_user_connected_and_favorite_not_recorded(self):

        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        subs = Products.objects.create(name="Prince goût chocolat", code="7622210449283")
        prod = Products.objects.create(name="Véritable petit beurre", code="7622210988034")

        response_login = self.client.login(username= 'lennon@thebeatles.com', password= 'johnpassword')

        response_post = self.client.post("/save/7622210988034/7622210449283")

        fav = Favorites.objects.all()

        assert response_login == True
        assert response_post.status_code == 200
        assert response_post.templates[0].name == "food_substitute/favorites.html"
        assert response_post.context["recording"] == True
        assert response_post.context["duplicates"] == False
        assert response_post.context["user"] == user
        assert fav[0].products.name == "Véritable petit beurre"
        assert fav[0].substitute.name == "Prince goût chocolat"
        assert fav[0].users.email == "lennon@thebeatles.com"


    @mark.django_db
    def test_save_user_not_connected(self):

        subs = Products.objects.create(name="Prince goût chocolat", code="7622210449283")
        prod = Products.objects.create(name="Véritable petit beurre", code="7622210988034")

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
    subs = Products.objects.create(name="Prince goût chocolat", code="7622210449283")
    prod = Products.objects.create(name="Véritable petit beurre", code="7622210988034")

    fav = Favorites.objects.create(
                                    users = user,
                                    products = prod,
                                    substitute = subs,
                                    )

    response_login = client.login(username= 'lennon@thebeatles.com', password= 'johnpassword')

    response_post = client.get("/favorites/")

    assert response_login == True
    assert response_post.status_code == 200
    assert response_post.templates[0].name == "food_substitute/favorites.html"
    assert response_post.context['recording'] == False
    assert response_post.context["favorite_recorded"][0][0].name == "Véritable petit beurre"
    assert response_post.context["favorite_recorded"][0][1].name == "Prince goût chocolat"