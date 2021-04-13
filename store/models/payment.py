from django.db import models # importing the model library from the django database
from django.contrib.auth.models import User
from .order import Order
from .product import Product


class Payment(models.Model):
    order = models.ForeignKey(Order , on_delete = models.CASCADE)
    date = models.DateTimeField(null= False , auto_now_add=True)
    payment_status = models.CharField(max_length=15 , default='FAILED')
    payment_id = models.CharField(max_length=60)
    payment_request_id = models.CharField(max_length=60 , unique=True , null=False)