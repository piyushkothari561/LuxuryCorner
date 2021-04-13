from django.db import models # importing the model library from the django database
from django.contrib.auth.models import User
from .size import SizeVariant
from .product import Product



class Order(models.Model):
    orderStatus =  (
        ('PENDING' , "Pending"), 
        ('PLACED' , "Placed"), 
        ('CANCELED' , "Canceled"), 
        ('COMPLETED' , "Completed"), 
    )
    method =  (
        ('ONLINE' , "Online"), 
    )
    order_status = models.CharField(max_length=15 , choices=orderStatus)
    payment_method = models.CharField(max_length=20 , choices=method)
    shipping_address = models.CharField(max_length=100  , null = False)
    phone = models.CharField(max_length=10 , null=False )
    user = models.ForeignKey(User , on_delete = models.CASCADE)
    total = models.IntegerField(null=False)
    date = models.DateTimeField(null= False , auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order , on_delete = models.CASCADE)
    product = models.ForeignKey(Product , on_delete = models.CASCADE)
    size = models.ForeignKey(SizeVariant , on_delete = models.CASCADE)
    quantity = models.IntegerField(null=False) 
    price = models.IntegerField(null=False) 
    date = models.DateTimeField(null= False , auto_now_add=True)
