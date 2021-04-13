from django.db import models # importing the model library from the django database
from django.contrib.auth.models import User
from .product import Product

class SizeVariant(models.Model):
    SIZES = (
        ('S' , "Small"), 
        ('M' , "Medium"), 
        ('L' , "Large")
    )
    price = models.IntegerField(null = False)
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    size = models.CharField(choices=SIZES , max_length=5)

    def __str__(self):
        return f'{self.size}'

