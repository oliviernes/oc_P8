from django.db import models

# Create your models here.

class category(models.Model):
    name=models.CharField(max_length=150)

class products(models.Model):
    code = models.CharField(max_length=13)
    category=models.ForeignKey(category, on_delete=models.CASCADE)
