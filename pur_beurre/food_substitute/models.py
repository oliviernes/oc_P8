from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=150)


class Products(models.Model):
    code = models.CharField(max_length=13)
    category = models.ManyToManyField(Category)
    name = models.CharField(max_length=255, null=True)
    nutrition_grades = models.CharField(max_length=255, null=True)
    image_front = models.CharField(max_length=255, null=True)
    image_front_thumb = models.CharField(max_length=255, null=True)
    image_nutrition = models.CharField(max_length=255, null=True)
    url = models.CharField(max_length=255, null=True)
