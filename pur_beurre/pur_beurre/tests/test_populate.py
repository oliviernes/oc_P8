from pytest import fixture, mark

from food_substitute.management.commands.populate_db import Command
from food_substitute.models import Products

@mark.django_db
def test_duplicate_products():
    products_db=Products.objects.all()
    code_list=[products_db[i].code for i in range(len(products_db))]
    code_unique_list=set(code_list)
    assert len(code_list)==len(code_unique_list)
