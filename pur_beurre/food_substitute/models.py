from django.db import models

# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=150)

class Products(models.Model):
    code = models.CharField(max_length=13)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
