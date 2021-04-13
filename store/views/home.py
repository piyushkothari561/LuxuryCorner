from store.models import Product,Order, OrderItem, Payment, ProductProperty, Gender, Brand, Colour, Categorie, SizeVariant, Cart
from django.shortcuts import render, redirect, HttpResponse
from django.core.paginator import Paginator
from urllib.parse import urlencode

def home(request): 
  
      query =  request.GET
      product = []
      products = Product.objects.all()
      brand = query.get('brand')
      category = query.get('category')
      gender = query.get('gender')
      colour = query.get('colour')

      if brand!= '' and brand is not None:
         products = products.filter(brand__slug=brand)
      if category != '' and category is not None:
         products = products.filter(category__slug=category)
      if colour != '' and colour is not None:
         products = products.filter(colour__slug=colour)
      if gender != '' and gender is not None:
         products = products.filter(gender__slug=gender)

      category = Categorie.objects.all()
      brands = Brand.objects.all()
      gender = Gender.objects.all()
      colour = Colour.objects.all()
      #print(products)
      #print(len(products))

      cart = request.session.get('cart')

      context = {
         "products" : products, "category" :category, 
         "brands" :brands, "gender": gender, "colour": colour
      }

      return render(request, template_name='store/index.html', context=context)

def items(request): 
  
      query =  request.GET
      product = []
      products = Product.objects.all()
      brand = query.get('brand')
      category = query.get('category')
      gender = query.get('gender')
      colour = query.get('colour')
      page = query.get('page')
      if(page is None or page == ''):
          page = 1
      if brand!= '' and brand is not None:
         products = products.filter(brand__slug=brand)
      if category != '' and category is not None:
         products = products.filter(category__slug=category)
      if colour != '' and colour is not None:
         products = products.filter(colour__slug=colour)
      if gender != '' and gender is not None:
         products = products.filter(gender__slug=gender)

      category = Categorie.objects.all()
      brands = Brand.objects.all()
      gender = Gender.objects.all()
      colour = Colour.objects.all()
      #print(products)
      #print(len(products))

      cart = request.session.get('cart')

      paginator = Paginator(products , 12)
      page_object = paginator.get_page(page)

      query = request.GET.copy()
      query['page'] = ''
      pageurl = urlencode(query)

      context = {
         "page_object" : page_object, "category" :category, 
         "brands" :brands, "gender": gender, "colour": colour, 'pageurl' : pageurl
      }

      return render(request, template_name='store/items.html', context=context)

