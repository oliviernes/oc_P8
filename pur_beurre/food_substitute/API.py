#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from .models import Products


def product_data(code):

    # ~ search_param = {
    # ~ "code": 5411188119098,
    # ~ "json": 1,
    # ~ }

    # ~ API_URL = "https://fr-en.openfoodfacts.org/cgi/search.pl?"

    API_URL = "https://fr.openfoodfacts.org/api/v0/product/" + str(code) + ".json"

    # ~ req = requests.get(API_URL, params=search_param)

    # ~ req = requests.get('https://fr.openfoodfacts.org/api/v0/product/5411188119098.json')

    req = requests.get(API_URL)

    req_output = req.json()

    data_prod = {
        "name": req_output["product"]["product_name_fr"],
        "image_front": req_output["product"]["image_front_url"],
        "image_nutrition": req_output["product"]["image_nutrition_url"],
        "nutrition_grades": req_output["product"]["nutrition_grades"],
        "ingredients_list": req_output["product"]["ingredients_text_fr"],
    }

    url = "https://fr.openfoodfacts.org/[code]/[name]"

    return data_prod


# ~ data=product_data(5411188119098)
