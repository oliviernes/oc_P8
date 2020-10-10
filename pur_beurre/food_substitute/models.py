"""food_substitute models"""
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    """Record Category model"""
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Products(models.Model):
    """Record Products model"""
    code = models.CharField(max_length=13)
    category = models.ManyToManyField(Category)
    name = models.CharField(max_length=255, null=True)
    nutrition_grades = models.CharField(max_length=255, null=True)
    image = models.URLField(null=True)
    image_small = models.URLField(null=True)
    image_nutrition = models.URLField(null=True)
    url = models.URLField(max_length=255, null=True)

    def display_category(self):
        """Create a string for the Category.
         This is required to display category in Admin.
        """
        return ", ".join(category.name for category in self.category.all()[:3])

    display_category.short_description = "Category"

    def __str__(self):
        return self.name


class Favorites(models.Model):
    """Record Favorites model"""
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name="prod_id"
    )
    substitute = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name="subs_id"
    )
