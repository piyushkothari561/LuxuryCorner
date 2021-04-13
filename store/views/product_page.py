from django.shortcuts import render, redirect, HttpResponse
from store.forms.authforms import CustomerCreationForm, CustomerAuthForm
from store.forms.checkout_form import CheckForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as loginUser, logout
from store.models import Product,Order, OrderItem, Payment, ProductProperty, Gender, Brand, Colour, Categorie, SizeVariant, Cart
from math import floor
from django.views.generic.detail import DetailView

                                
class ProductDetailView(DetailView):
    template_name = 'store/product_details.html'
    model = Product
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context.get('product') 
        request = self.request
        size = request.GET.get('size')
        if size is None:
            size = product.sizevariant_set.all().order_by('price').first()
        else:
            size = product.sizevariant_set.get(size=size)

        size_price = floor(size.price)

        sell_price = size_price - (size_price * (product.discount / 100))
        sell_price = floor(sell_price)

        context = {
            'product': product,
            'price': size_price,
            'sell_price': sell_price,
            'active_size': size
        }
        return context