from django.db import models # importing the model library from the django database
from django.contrib.auth.models import User
from .size import SizeVariant
from .product import Product

        
class Cart(models.Model):
    sizeVariant = models.ForeignKey(SizeVariant , on_delete = models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User , on_delete = models.CASCADE) 
