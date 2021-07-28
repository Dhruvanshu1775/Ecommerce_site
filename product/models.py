from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.


class ProductCategory(models.Model):
    name = models.CharField(max_length = 24)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name         = models.CharField(max_length = 24)
    category_key = models.ForeignKey(ProductCategory, on_delete = models.CASCADE )

    def __str__(self):
        return  self.name


class ProductDetail(models.Model):
    product_name        = models.CharField(max_length = 250)
    product_pic         = models.ImageField(upload_to = 'product/pic')
    product_price       = models.IntegerField()
    product_old_price   = models.IntegerField()
    product_category    = models.ForeignKey(ProductCategory, on_delete = models.CASCADE)
    product_brand       = models.ForeignKey(Brand, on_delete = models.CASCADE)
    product_description = models.TextField()
    product_stock       = models.IntegerField()

    def __str__(self):
        return self.product_name + "  --->    Total No. Of Stock  " + str(self.product_stock)

    def trim_data(self):
        return self.product_name[:50]

class AddToCard(models.Model):
    user_key         = models.ForeignKey(User, on_delete = models.CASCADE)
    product_key      = models.ForeignKey(ProductDetail, on_delete = models.CASCADE)
    is_wishlist      = models.BooleanField(default = False)
    product_quantity = models.IntegerField(blank = True, null = True)

    def __str__(self):
        return str(self.product_key)

class PaymentMode(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name

class city(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name

class Order(models.Model):
    order_id      = models.CharField(max_length = 5,blank=True,editable=False,unique=True,default=uuid.uuid4)
    user_key      = models.ForeignKey(User, on_delete = models.CASCADE)
    payment_key   = models.ForeignKey(PaymentMode, on_delete = models.CASCADE, blank = True, null = True)
    product_key   = models.ForeignKey(AddToCard, on_delete = models.CASCADE)
    quantity      = models.IntegerField()
    city_key      = models.ForeignKey(city, on_delete = models.CASCADE)
    time_stamp    = models.DateTimeField(auto_now_add = True)
    address       = models.TextField()
    first_name    = models.CharField(max_length = 100)
    last_name     = models.CharField(max_length = 100)
    email         = models.EmailField()
    phone_number  = models.IntegerField()
    total_price   = models.IntegerField()
    zip_code      = models.IntegerField()
    is_delivered  = models.BooleanField(default = False)
    is_cancel     = models.BooleanField(default = False)
    is_processing = models.BooleanField(default = False)

    def __str__(self):
        return str(self.user_key)

class Compare(models.Model):
    user_key    = models.ForeignKey(User, on_delete = models.CASCADE)
    product_key = models.ForeignKey(ProductDetail, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.user_key)

class Review(models.Model):
    user_key    = models.ForeignKey(User, on_delete = models.CASCADE)
    product_key = models.ForeignKey(ProductDetail, on_delete = models.CASCADE)
    rating      = models.FloatField()
    comment     = models.TextField()

    def __str__(self):
        return str(self.user_key)
