from django.urls import path

from . import views

urlpatterns = [
    path("", views.welcome, name="welcome"),
    path("product/<code>", views.detail, name="detail"),
    path("disclaimer/", views.disclaimer, name="disclaimer"),
    path("search/", views.search, name="search"),
]
