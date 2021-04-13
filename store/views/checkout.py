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

def cal_total_payable_amount(cart):
    total = 0
    for c in cart:

        discount = c.get('product').discount
        price = c.get('size').price
        sale_price = floor(price - (price * (discount / 100)))
        total_of_single_product = sale_price * c.get('quantity')
        total = total + total_of_single_product

    return total

@login_required(login_url= '/login/')
def checkout(request):
    if request.method == 'GET':
        form = CheckForm()
        cart = request.session.get('cart')
        if cart is None:
            cart = []

        for c in cart:
            size_str = c.get('size')
            product_id = c.get('product')
            size_obj = SizeVariant.objects.get(size=size_str, product=product_id)
            c['size'] = size_obj
            c['product'] = size_obj.product


        return render(request, 'store/checkout.html', {
            "form": form,
            'cart': cart
        })
    else:
         form = CheckForm(request.POST)
         user = None
         if request.user.is_authenticated:
            user = request.user
         if form.is_valid():
            cart = request.session.get('cart')
            if cart is None :
                cart : []
            for c in cart:
                size_str = c.get('size')
                product_id = c.get('product')
                size_obj = SizeVariant.objects.get(size=size_str, product=product_id)
                c['size'] = size_obj
                c['product'] = size_obj.product    
            shipping_address = form.cleaned_data.get('shipping_address')
            phone = form.cleaned_data.get('phone')
            payment_method = form.cleaned_data.get('payment_method')
            total = cal_total_payable_amount(cart)
            print(shipping_address, phone, payment_method, total )
            order = Order()
            order.shipping_address = shipping_address
            order.phone = phone
            order.payment_method = payment_method
            order.total = total
            order.order_status = "PENDING"
            order.user = user
            order.save()

    

            for c in cart:
                 order_item = OrderItem()
                 order_item.order = order
                 size = c.get('size')
                 product = c.get('product')
                 order_item.price = floor(size.price -
                                         (size.price *
                                          (product.discount / 100)))
                 order_item.quantity = c.get('quantity')
                 order_item.size = size
                 order_item.product = product
                 order_item.save()

        # Create a new Payment Request
            response = API.payment_request_create(
            amount=order.total,
            purpose='Payment for Products',
            send_email=True,
            buyer_name=f'{user.first_name} {user.last_name}' ,
            email=user.email,
            redirect_url="http://localhost:8000/validate_payment"
            )
            print(response['payment_request'])
            payment_request_id = response['payment_request']['id']
            url = response['payment_request']['longurl']

            payment = Payment()
            payment.order = order
            payment.payment_request_id = payment_request_id
            payment.save()

            return redirect(url)
         else:
            return redirect('/checkout/')

