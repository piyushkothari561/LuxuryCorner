from django.db import models # importing the model library from the django database
from django.contrib.auth.models import User
from .product_properties import ProductProperty, Gender, Brand, Colour, Categorie

class Product(models.Model):
    name = models.CharField(max_length=50 , null=False)
    slug = models.CharField(max_length=200 , null=False, unique=True, default="")
    description = models.CharField(max_length=500 , null=True)
    discount = models.IntegerField(default=0)
    image = models.ImageField(upload_to ='upload/images/' , null=False)
    category = models.ForeignKey(Categorie , on_delete = models.CASCADE)
    brand = models.ForeignKey(Brand , on_delete = models.CASCADE)
    gender = models.ForeignKey(Gender , on_delete = models.CASCADE)
    colour = models.ForeignKey(Colour , on_delete = models.CASCADE)
    def __str__(self):
        return self.name 
