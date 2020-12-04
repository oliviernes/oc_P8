"""Register models """
from django.contrib import admin

from .models import Products, Category

admin.site.register(Category)


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    """Register the Products classes using the decorator"""

    list_display = ("name", "nutrition_grades", "display_category")
    list_filter = ["nutrition_grades"]
