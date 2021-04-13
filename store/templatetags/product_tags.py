from django import template
from math import floor

register = template.Library()

@register.filter
def usd(number):
    return f'₹{number}'

@register.filter
def cal_total_payable_amount(cart):
    total = 0
    for c in cart:
        discount = c.get('product').discount
        price = c.get('size').price
        sale_price = clc_sale_price(price , discount)
        total_of_single_product = sale_price * c.get('quantity')
        total = total + total_of_single_product
        
    return total



@register.simple_tag
def min_price(product):
    size = product.sizevariant_set.all().order_by('price').first()
    return floor(size.price)
    
@register.simple_tag
def multiply(a,b):
   return a*b 


@register.simple_tag
def clc_sale_price(price, discount):
   return floor(price - (price * (discount/100 ))) 


@register.simple_tag
def sale_price(product):
    price = min_price(product)
    discount = product.discount
    return floor(price - (price * (discount / 100)))

@register.simple_tag
def get_active_size_button_class(active_size, size):
        if active_size == size:
            return "dark"
        
        return "light"

     
