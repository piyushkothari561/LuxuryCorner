from django.shortcuts import render, redirect, HttpResponse
from store.forms.authforms import CustomerCreationForm, CustomerAuthForm
from store.forms.checkout_form import CheckForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as loginUser, logout
from store.models import Product,Order, OrderItem, Payment, ProductProperty, Gender, Brand, Colour, Categorie, SizeVariant, Cart

from django.views.generic.list import ListView
    


class OrderListView(ListView):
    template_name = 'store/orders.html'
    model = Order
    paginate_by = 3
    context_object_name = 'orders'

    def get_queryset(self):
        return  Order.objects.filter(user = self.request.user).order_by('-date').exclude(
        order_status='PENDING')