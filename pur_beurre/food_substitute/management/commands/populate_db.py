from django.core.management.base import BaseCommand, CommandError
from food_substitute.models import Category, Products
from food_substitute.config import CATEGORIES

import requests


class Command(BaseCommand):
    help = "Populate the db with products' data using the Openfoodfacts API"

    def search_data(self, category):

        "Search product's data for a given category over the API openfoodfacts"

        search_param = {
            "search_terms": category,
            "search_tag": "categories_tag",
            "sort_by": "unique_scans_n",
            "page_size": 250,
            "json": 1,
        }

        API_URL = "https://fr-en.openfoodfacts.org/cgi/search.pl?"

        req = requests.get(API_URL, search_param)

        # output of request as a json file
        req_output = req.json()

        prod_cat = req_output["products"]

        return prod_cat

    def populate(self, infos_prod, categor):
        "Populate the DB with the first 250 products of a category \
from the API"

        if len(infos_prod) > 0:
                cat = Category(name=categor)
                cat.save()
                print(f"The category {cat.name} has been insterted in the DB")    
                for i in range(250):
                    prod_index = infos_prod[i]
                    """Add an if statements to not duplicate products entry in the db"""
                    if len(Products.objects.filter(code=prod_index["code"])) == 0:
                        prod = Products(code=prod_index["code"])
                        prod.name = prod_index.get("product_name_fr", "")
                        prod.image = prod_index.get("image_url", "")
                        prod.image_small = prod_index.get(
                            "image_small_url", ""
                        )
                        prod.image_nutrition = prod_index.get("image_nutrition_url", "")
                        prod.nutrition_grades = prod_index.get("nutrition_grades", "")
                        prod.url = prod_index.get("url", "")
                        prod.save()
                        prod.category.add(Category.objects.get(id=cat.id))
                        prod.save()
                        print(
                            f"The product {prod.name} has been inserted in \
the DB"
                        )
                    else:
                        prod = Products.objects.get(code=prod_index["code"])
                        prod.category.add(Category.objects.get(id=cat.id))
        else:
            print(
                f"The category {categor} is not present in OFF\
    API. No products will be inserted in the database"
            )

    def handle(self, *args, **options):

        for categor in CATEGORIES:
            infos_prod = self.search_data(categor)
            self.populate(infos_prod, categor)
