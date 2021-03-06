"""Map URL patterns to view function"""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.welcome, name="welcome"),
    path("product/<code>", views.detail, name="detail"),
    path("disclaimer/", views.disclaimer, name="disclaimer"),
    path("search/", views.search, name="search"),
    path("favorites/", views.favorites, name="favorites"),
    path("save/<produc>/<substitut>", views.save, name="save"),
]
