from django.test import Client
from django.contrib.auth.models import User

from pytest import mark

from food_substitute.models import Category, Products, Favorites

####################
### Cagetory model #
####################

@mark.django_db
def test_category_name_label():

    Category.objects.create(name='biscuits')
    categor = Category.objects.get(id=1)
    field_label = categor._meta.get_field('name').verbose_name
    assert field_label == 'name'

####################
### Product model  #
####################

@mark.django_db
def test_products_labels():

    Products.objects.create(
                            code='456465',
                            name='petit Beurre',
                            nutrition_grades='D',
                            image="https://static.openfoodfacts.org/images/products/339/039/000/1259/front_fr.33.400.jpg",
                            image_small= "https://static.openfoodfacts.org/images/products/339/039/000/1259/front_fr.33.200.jpg",
                            image_nutrition= "https://static.openfoodfacts.org/images/products/339/039/000/1259/nutrition_fr.40.400.jpg",
                            url= "https://fr-en.openfoodfacts.org/product/3390390001259/chocolade-sans-lait-40-noisette-jean-herve",
                            )

    prod = Products.objects.get(id=1)
    code_label = prod._meta.get_field('code').verbose_name
    name_label = prod._meta.get_field('name').verbose_name
    nutrition_grades_label = prod._meta.get_field('nutrition_grades').verbose_name
    image_label = prod._meta.get_field('image').verbose_name
    image_small_label = prod._meta.get_field('image_small').verbose_name
    image_nutrition_label = prod._meta.get_field('image_nutrition').verbose_name
    url_label = prod._meta.get_field('url').verbose_name
    assert code_label == 'code'
    assert name_label == 'name'
    assert nutrition_grades_label == 'nutrition grades'
    assert image_label == 'image'
    assert image_small_label == 'image small'
    assert image_nutrition_label == 'image nutrition'
    assert url_label == 'url'