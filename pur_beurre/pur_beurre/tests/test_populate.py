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


## test giving a false positive, not deleted for studying purpose
@mark.django_db
def test_duplicate_products():
    """Test if the database have duplicate products"""

    products_db = Products.objects.all()
    code_list = [products_db[i].code for i in range(len(products_db))]
    code_unique_list = set(code_list)

    assert len(code_list) == len(code_unique_list)


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
    prod = Products.objects.all()[0]

    assert prod.code == "3017620422003"
    assert prod.name == ""
    assert prod.url == ""
    assert prod.image_small == ""


@mark.django_db
def test_printing_category_inserted(db_feed, nutella, capsys):
    """ test the printing of inserted categories """
    Fake_API_response = [nutella[1]["fields"]]
    Products.objects.create(code="3017620420047")

    db_feed.populate(Fake_API_response, "pâtes à tartiner au chocolat")

    out, err = capsys.readouterr()
    assert (
        out
        == "The category pâtes à tartiner au chocolat has been \
insterted in the DB\n"
    )

@mark.django_db
def test_printing_category_already_been_inserted(db_feed, nutella, capsys):
    """ test the printing of inserted categories """
    Fake_API_response = [nutella[1]["fields"]]
    Products.objects.create(code="3017620420047")
    Category.objects.create(name="pâtes à tartiner au chocolat")

    db_feed.populate(Fake_API_response, "pâtes à tartiner au chocolat")

    out, err = capsys.readouterr()
    assert (
        out
        == "The category pâtes à tartiner au chocolat has already been \
insterted in the DB\n"
    )

@mark.django_db
def test_product_with_long_fields(db_feed, nutella):

    Fake_API_response = [nutella[2]["fields"]]

    db_feed.populate(Fake_API_response, "category")
    prod = Products.objects.all()[0]

    assert prod.code == "3017620425035"
    assert (
        prod.name
        == "NutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNutellaNut"
    )
