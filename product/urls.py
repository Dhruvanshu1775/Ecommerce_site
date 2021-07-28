from django.urls import path

from .views import productpage, addproduct, finalcart, searchbar, addwishlist, deletecart, product_detail, Checkout, ConfirmOrder, myorders, send_mail, searchbrand, delete_all_cart, CompareProduct, CompareView
from .views import rating, tracking, delete_compare_list

app_name = 'product'

urlpatterns = [
    path('product-page/', productpage, name = 'productpage'),
    path('addproduct/', addproduct, name = 'addproduct'),
    path('finalcart/', finalcart, name = 'finalcart'),
    path('searchbar/', searchbar, name = 'searchbar'),
    path('addwishlist/', addwishlist, name = 'wishlist'),
    path('deletecart/<int:id>', deletecart, name = 'deletecart'),
    path('product_detail/<int:id>', product_detail, name = 'product_detail'),
    path('checkout/', Checkout, name = 'checkout'),
    path('confirmorder/', ConfirmOrder, name = 'confirmorder'),
    path('myorders/', myorders, name = 'myorders'),
    path('send_mail/', send_mail, name = 'send_mail'),
    path('searchbrand/', searchbrand, name = 'searchbrand'),
    path('delete_all_cart/', delete_all_cart, name = 'cart_delete'),
    path('compare-product/', CompareProduct, name = 'compareproduct'),
    path('compare-view/', CompareView, name = 'compareview'),
    path('rating/<int:id>', rating, name = 'rating'),
    path('tracking/', tracking, name = 'tracking'),
    path('delete_compare_list/', delete_compare_list, name = 'delete_compare_list')
]
