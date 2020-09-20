from django.contrib import admin

from .models import Products, Category

admin.site.register(Category)

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'nutrition_grades', 'display_category')
