from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=150)


class Products(models.Model):
    code = models.CharField(max_length=13)
    category = models.ManyToManyField(Category)
    name = models.CharField(max_length=255, null=True)
    nutrition_grades = models.CharField(max_length=255, null=True)
    image_front = models.URLField(null=True)
    image_front_thumb = models.URLField(null=True)
    image_nutrition = models.URLField(null=True)
    url = models.URLField(null=True)
