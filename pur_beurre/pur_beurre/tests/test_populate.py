import json

import unittest
from unittest.mock import patch

from pytest import fixture, mark

from food_substitute.management.commands.populate_db import Command
from food_substitute.models import Products, Category


@fixture
def nutella():
    """Mock API response of nutella products"""

    nutella_file = "pur_beurre/tests/nutella.json"

    with open(nutella_file, "r") as json_file:
        json_response_from_api = json.load(json_file)

    return json_response_from_api


@fixture
def db_feed():
    return Command()


@patch('food_substitute.management.commands.populate_db.requests.get')
def test_search_data(mock_request):
    mock_request.return_value.json.return_value = {
                                    "products": {
                                        "code": "3017620422003",
                                        "category": [
                                            274,
                                            250
                                        ]
                                    }
                                }

    results = Command().search_data("pâtes à tartiner au chocolat")

    assert results == {
        "code": "3017620422003",
        "category": [
            274,
            250
        ]
    }


@mark.django_db
def test_fields_missing(db_feed, nutella):
    """Test if a product with missing fields can populate the db and \
if the length of the API's answer is <250 products"""

    Fake_API_response = [nutella[0]["fields"]]

    db_feed.populate(Fake_API_response, "category")
    products = Products.objects.all()
    prod = Products.objects.all()[0]

    assert products.count() == 1
    assert prod.code == "3017620422003"
    assert prod.name == ""
    assert prod.url == ""
    assert prod.image_small == ""

@mark.django_db
def test_product_insertion(db_feed, nutella):

    Fake_API_response = [nutella[1]["fields"]]

    db_feed.populate(Fake_API_response, "pâtes à tartiner au chocolat")
    cat = Category.objects.get(name = "pâtes à tartiner au chocolat")
    productos = Products.objects.all()
    prod = Products.objects.all()[0]
    relation = cat.products_set.all()
    prodn = Category.objects.filter(products__name = "Nutella")

    assert productos.count() == 1
    assert prod.code == "3017620420047"
    assert prod.name == "Nutella"
    assert prod.nutrition_grades == "e"
    assert prod.image == "https://static.openfoodfacts.org/images/products/301/762/042/0047/front_fr.140.400.jpg"
    assert prod.image_small == "https://static.openfoodfacts.org/images/products/301/762/042/0047/front_fr.140.200.jpg"
    assert prod.image_nutrition == "https://static.openfoodfacts.org/images/products/301/762/042/0047/nutrition_fr.124.400.jpg"
    assert prod.url == "https://fr-en.openfoodfacts.org/product/3017620420047/nutella-ferrero"
    assert relation[0].name == "Nutella"

@mark.django_db
def test_printing_category_inserted(db_feed, nutella, capsys):
    Fake_API_response = [nutella[1]["fields"]]
    Products.objects.create(code="3017620420047")

    db_feed.populate(Fake_API_response, "pâtes à tartiner au chocolat")

    cat = Category.objects.all()

    out, err = capsys.readouterr()
    assert (
        out
        == "The category pâtes à tartiner au chocolat has been \
insterted in the DB\n"
    )
    assert cat.count() == 1
    assert cat[0].name == "pâtes à tartiner au chocolat"

@mark.django_db
def test_printing_category_already_been_inserted(db_feed, nutella, capsys):
    Fake_API_response = [nutella[1]["fields"]]
    Products.objects.create(code="3017620420047")
    Category.objects.create(name="pâtes à tartiner au chocolat")

    db_feed.populate(Fake_API_response, "pâtes à tartiner au chocolat")

    cat = Category.objects.all()

    out, err = capsys.readouterr()
    assert (
        out
        == "The category pâtes à tartiner au chocolat has already been \
insterted in the DB\n"
    )
    assert cat.count() == 1


@mark.django_db
def test_printing_category_not_in_OFF(db_feed, nutella, capsys):
    Fake_API_response = []
    Products.objects.create(code="3017620420047")
    
    db_feed.populate(Fake_API_response, "pasta à tartiner au chocolat")

    cat = Category.objects.all()

    out, err = capsys.readouterr()
    assert (
        out
        == "The category pasta à tartiner au chocolat is not present in OFF\
    API. No products will be inserted in the database\n"
    )
    assert cat.count() == 0

@mark.django_db
def test_product_with_long_fields(db_feed, nutella):

    Fake_API_response = [nutella[2]["fields"]]

    db_feed.populate(Fake_API_response, "category")
    prod = Products.objects.all()[0]

    cat = Category.objects.all()

    assert prod.code == "3017620425035"
    assert (
        prod.name
        == "NutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNut"
    )
    assert cat.count() == 1
    assert cat[0].name == "category"
