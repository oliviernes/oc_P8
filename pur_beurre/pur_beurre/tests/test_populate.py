import json

from pytest import fixture, mark

from food_substitute.management.commands.populate_db import Command
from food_substitute.models import Products

@fixture
def nutella():
    """Mock API response of nutella products"""
    
    nutella_file="pur_beurre/tests/nutella.json"
    
    with open(nutella_file, "r") as json_file:
        json_response_from_api = json.load(json_file)
    
    return json_response_from_api

@fixture
def db_feed():
    return Command()
   
@mark.django_db
def test_duplicate_products():
    """Test if the database have duplicate products"""

    products_db=Products.objects.all()
    code_list=[products_db[i].code for i in range(len(products_db))]
    code_unique_list=set(code_list)

    assert len(code_list)==len(code_unique_list)

@mark.django_db
def test_fields_missing(db_feed, nutella):
    
    category="pâtes à tartiner au chocolat"
    Fake_API_response=[nutella[0]['fields']]
    
    db_feed.populate(Fake_API_response, category)
    prod=Products.objects.all()[0]
    
    assert prod.code == "3017620422003"
    assert prod.name == ""
    assert prod.url == ""
    assert prod.image_small ==""    
