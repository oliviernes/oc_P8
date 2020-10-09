# pur_beurre startup:

The startup Pur Beurre want to develop a web platform for their customers in order to help them find an healthier substitute for a product too fatty, too sweet or too salty.

# Created with:

* Python 3.7.4
* Django 3.0.4

# Heroku:

The `Procfile` provided allows to deploy the program on heroku.

# How to run the program:

For linux local storage:

* fork the code
* cd oc_P8
* Create a virtual environement: virtualenv -p python3 .venv
* Activate the virtual environment: source .venv/bin/activate
* cd pur_beurre
* python3 manage.py runserver

The website is accessible on http://127.0.0.1:8000/ with your web browser.

# Tests:

You can test the program with the following commands:

* functional tests: python3 manage.py test functional_tests/

* unit tests and integration test: pytest

* For coverage: coverage run -m --omit=../.venv*,test*,food_substitute/migr* pytest

