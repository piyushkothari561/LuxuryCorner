
from django.contrib import admin
from django.urls import path
from store.views import home, cart, checkout, add_to_cart, LoginView, OrderListView, signup, signout, ProductDetailView, validatePayment, deleteCart, items
from django.contrib.auth.decorators import login_required

#django admin header customization
admin.site.site_header = "LuxuryCorner"
admin.site.site_title = "LuxuryCorner Admin "
admin.site.index_title= "LuxuryCorner Admin Dashboard"

urlpatterns = [
        path('', home , name='homepage'),
        path('home/', home),
        path('items/', items),
        path('cart/', cart ),
        path('login/', LoginView.as_view(), name='login' ),
        path('orders/' , login_required(OrderListView.as_view() , login_url='/login/') , name='orders' ), 
        path('signup/', signup ),
        path('checkout/', checkout),
        path('logout/', signout ),
        path("deleteCart", deleteCart, name="deleteCart"),
        path('product/<str:slug>', ProductDetailView.as_view()),
        path('addtocart/<str:slug>/<str:size>', add_to_cart),
        path('validate_payment', validatePayment)
]
