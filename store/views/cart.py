from django.shortcuts import render, redirect, HttpResponse
from store.forms.authforms import CustomerCreationForm, CustomerAuthForm
from store.forms.checkout_form import CheckForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as loginUser, logout
from store.models import Product,Order, OrderItem, Payment, ProductProperty, Gender, Brand, Colour, Categorie, SizeVariant, Cart
from math import floor
from instamojo_wrapper import Instamojo
from django.contrib.auth.decorators import login_required
from LuxuryCorner.settings import API_KEY, AUTH_TOKEN

API = Instamojo(api_key=API_KEY,
                auth_token=AUTH_TOKEN,
                endpoint='https://test.instamojo.com/api/1.1/')

def cart(request):
    cart = request.session.get('cart')
    if cart is None:
        cart = []

    for c in cart:
        product_id = c.get('product')
        product = Product.objects.get(id=product_id)
        c['size'] = SizeVariant.objects.get(product=product_id, size=c['size'])
        c['product'] = product

    return render(request,
                  template_name='store/cart.html',
                  context={'cart': cart})

def add_to_cart(request, slug, size):
    user = None
    if request.user.is_authenticated:
        user = request.user
    cart = request.session.get('cart')
    if cart is None:
        cart = []

    product = Product.objects.get(slug=slug)
    add_cart_for_anom_user(cart, size, product)
    if user is not None:
        add_cart_to_database(user, size, product)

    request.session['cart'] = cart
    return_url = request.GET.get('return_url')
    return redirect(return_url)


def add_cart_to_database(user, size, product):
    size = SizeVariant.objects.get(size=size, product=product)
    existing = Cart.objects.filter(user=user, sizeVariant=size)

    if len(existing) > 0:
        obj = existing[0]
        obj.quantity = obj.quantity + 1
        obj.save()

    else:
        c = Cart()
        c.user = user
        c.sizeVariant = size
        c.quantity = 1
        c.save()

def add_cart_for_anom_user(cart, size, product):
    flag = True

    for cart_obj in cart:
        p_id = cart_obj.get('product')
        size_short = cart_obj.get('size')
        if p_id == product.id and size == size_short:
            flag = False
            cart_obj['quantity'] = cart_obj['quantity'] + 1

    if flag:
        cart_obj = {'product': product.id, 'size': size, 'quantity': 1}
        cart.append(cart_obj)




def deleteCart(request):
    user = None
    if request.user.is_authenticated:
        user = request.user
    cart = []
    request.session['cart'] = cart
    Cart.objects.filter(user=user).delete()    
    return redirect('/cart/')
