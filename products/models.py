from django.db import models

# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    image = models.CharField(max_length=500)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=3)
    description = models.CharField(max_length=10000)
