from django.contrib import admin

from .models import ProductDetail, ProductCategory, AddToCard, Order, PaymentMode, city, Brand, Compare, Review
# Register your models here.

admin.site.register(ProductDetail)
admin.site.register(ProductCategory)
admin.site.register(AddToCard)
admin.site.register(Order)
admin.site.register(PaymentMode)
admin.site.register(city)
admin.site.register(Brand)
admin.site.register(Compare)
admin.site.register(Review)
