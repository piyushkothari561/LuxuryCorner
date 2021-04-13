from django.contrib import admin
from store.models import Product, Cart, Gender, Brand, Colour, SizeVariant, Categorie, Order, OrderItem, Payment
from django.utils.html import format_html
# Register your models here.

class SizeVariantConfig(admin.TabularInline):
    model= SizeVariant
class OrderItemConfiguration(admin.TabularInline):
    model = OrderItem


class ProductConfig(admin.ModelAdmin):
    inlines = [ SizeVariantConfig ]
    list_display = ['get_image' , 'name' ,'discount']
    list_editable = ['discount']
    sortable_by = ['name']
    list_filter = ['discount']
    list_display_links = ['name']
    list_per_page = 10

    def get_image(self , obj):
        return format_html(f"""
                <a target='_blank' href='{obj.image.url}'><img height='100px' src='{obj.image.url}'/></a>
        """)
    get_image.short_description = 'Product Image'

class CartConfiguration(admin.ModelAdmin):
    model = Cart
    # fields = ( 'sizeVariant' , 'quantity', 'user' )
    list_display = ['quantity' , 'size' , 'product' , 'user' , 'username']

    fieldsets = (
        ("Cart Info" , { "fields" : ('user' , 'get_product' , 'get_sizeVariant' , 'quantity') } ), 
    )

    readonly_fields = ('quantity', 'user' , 'get_sizeVariant' , 'get_product' )
    
    def get_sizeVariant(self , obj):
            return obj.sizeVariant.size

    def get_product(self , obj):
        product = obj.sizeVariant.product
        product_id  = product.id 
        name = product.name
        return format_html(f'<a href="/admin/store/product/{product_id}/change/" target="_blank">{name}</a>')

    get_product.short_description = 'Product'
    get_sizeVariant.short_description = 'Size'

    def size(self , obj):
        return obj.sizeVariant.size
    
    def product(self , obj):
        return obj.sizeVariant.product.name 
    
    def username(self , obj):
        return obj.user.first_name


class OrderConfiguration(admin.ModelAdmin):
    list_display = ['user' , 'shipping_address' , 'phone' , 'date' , 'order_status' ]
    readonly_fields = (
        'user' , 'phone' , 
        'shipping_address' , 
        'user' , 'total', 
        'payment_method' , 'payment' , 'payment_request_id', 'payment_id' , 'payment_status' )
    
    fieldsets = (
        ("Order Information" , { "fields" : ( 'order_status' , 'shipping_address' , 'phone' , 'total' , 'user' ) } ),

        ("Payment Information" , { 'fields' : ('payment' , 'payment_request_id', 'payment_id' , 'payment_status') } )
    )
    inlines = [OrderItemConfiguration]

    def payment_request_id(self , obj):
        return  obj.payment_set.all()[0].payment_request_id
    
    def payment_status(self , obj):
        return  obj.payment_set.all()[0].payment_status

    def payment_id(self , obj):
        payment_id =   obj.payment_set.all()[0].payment_id
        if(payment_id is None or payment_id == ''):
            return "Payment Id is Not Available"
        else:
            return payment_id

    def payment(self , obj):
        payment_id = obj.payment_set.all()[0].id
        return format_html(f'<a href="/admin/store/payment/{payment_id}/change/" target="_blank">Click For Payment Information</a>')


admin.site.register(Product, ProductConfig )
admin.site.register(Gender)
admin.site.register(Brand)
admin.site.register(Categorie)
admin.site.register(Colour)
admin.site.register(Cart, CartConfiguration)
admin.site.register(Order, OrderConfiguration)
admin.site.register(OrderItem)
admin.site.register(Payment)
