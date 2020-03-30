from django.urls import path

from . import views

urlpatterns = [
    path("", views.welcome, name="welcome"),
    path("disclaimer/", views.disclaimer, name="disclaimer"),
]
