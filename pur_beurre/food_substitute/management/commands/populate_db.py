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

        prod_cat=req_output['products']

        return prod_cat
    
    def handle(self, *args, **options):
        
        for categor in CATEGORIES:
            infos_prod=self.search_data(categor)
            cat=Category(name='category')
            cat.save()
            print(f"The category {cat.name} has been insterted in the \
DB")
            for i in range(250):
                prod_index=infos_prod[i]
                prod=Products(code=prod_index['code'], \
category=Category.objects.get(id=cat.id),)
                prod.name=prod_index.get("product_name_fr", "")
                prod.image_front=prod_index.get('image_front_url', "")
                prod.image_front_thumb=prod_index.get('image_front_thumb_url', "")
                prod.image_nutrition=prod_index.get('image_nutrition_url', "")
                prod.nutrition_grades=prod_index.get('nutrition_grades', "")
                prod.save()
                print(f"The product {prod.name} has been inserted in \
the DB")
