from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Products(models.Model):
    code = models.CharField(max_length=13)
    category = models.ManyToManyField(Category)
    name = models.CharField(max_length=255, null=True)
    nutrition_grades = models.CharField(max_length=255, null=True)
    image = models.URLField(null=True)
    image_small = models.URLField(null=True)
    image_nutrition = models.URLField(null=True)
    url = models.URLField(max_length=255, null=True)

    def __str__(self):
        return self.name
