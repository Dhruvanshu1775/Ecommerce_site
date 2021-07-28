from django.shortcuts import render, redirect
from django.http import  JsonResponse
from django.contrib import messages
from django.db.models import Sum, Count
from .models import ProductDetail, ProductCategory, AddToCard, city, PaymentMode, Order, Brand, Compare, Review
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.db.models import Q

# Create your views here.

def productpage(request):


    product_obj = ProductDetail.objects.all()
    category_obj = ProductCategory.objects.all()
    add_cart_count = AddToCard.objects.filter(user_key = request.user, is_wishlist = False).count()
    add_wishlist_count = AddToCard.objects.filter(user_key = request.user, is_wishlist = True).count()




    context = {
        'product_obj':product_obj,
        'category_obj':category_obj,
        'add_cart_count':add_cart_count,
        'add_wishlist_count':add_wishlist_count,
    }

    return render(request, 'products.html', context)


def addproduct(request):
    product = request.POST['product']
    quantity = request.POST['quantity']

    product_detail = ProductDetail.objects.get(id = product)
    main_quantity = product_detail.product_stock

    add_obj = AddToCard.objects.filter(user_key = request.user)

    define_count = add_obj.filter(user_key = request.user, product_key = product)
    total = add_obj.filter(user_key = request.user,product_key = product).count()



    total2 = int(quantity)
    for data in define_count:
        total2 = total2  + int(data.product_quantity)

    print(total2)

    if int(quantity) == 0:
        data = {
            'messa':'Product Should Not be Zero bastard'
        }
        return JsonResponse(data)

    elif int(quantity) > int(main_quantity):
        data = {
            'mes':"Not In Stock" +" "+ "Total Stock : " + str(main_quantity)
        }
        return JsonResponse(data)

    elif int(total2) > int(main_quantity):
        data = {
            'message':"Out of Stock",
        }
        return JsonResponse(data)

    elif int(quantity) == int(main_quantity):
        addcart_obj = AddToCard()
        addcart_obj.product_quantity = quantity
        addcart_obj.user_key = request.user
        product_instance = ProductDetail.objects.get(pk = product)
        addcart_obj.product_key = product_instance
        addcart_obj.save()
    else:
        addcart_obj = AddToCard()
        addcart_obj.product_quantity = quantity
        addcart_obj.user_key = request.user
        product_instance = ProductDetail.objects.get(pk = product)
        addcart_obj.product_key = product_instance
        addcart_obj.save()


    add_cart_count = add_obj.filter(user_key = request.user, is_wishlist = False).count()
    data = {
        'add_cart_count':add_cart_count,
        'product_all_count':total2,
    }

    return JsonResponse(data)

def addwishlist(request):

    product = request.POST['product']

    if AddToCard.objects.filter(user_key = request.user, is_wishlist = True, product_key = product):
        print("nono")
    else:
        wislist_product = AddToCard()
        wislist_product.user_key = request.user
        product_instance = ProductDetail.objects.get(pk = product)
        wislist_product.product_key = product_instance
        wislist_product.is_wishlist = True
        wislist_product.save()

    add_wishlist_count = AddToCard.objects.filter(user_key = request.user, is_wishlist = True).count()


    data = {
        'add_wishlist_count':add_wishlist_count,
    }


    return JsonResponse(data)

def finalcart(request):

    add_obj = AddToCard.objects.filter(user_key = request.user, is_wishlist = False)
    add_cart_count = add_obj.count()
    add_wishlist_count = AddToCard.objects.filter(user_key = request.user, is_wishlist = True).count()


    context = {
        'add_obj':add_obj,
        'add_cart_count':add_cart_count,
        'add_wishlist_count':add_wishlist_count,
    }

    return render(request,'finalcart.html', context)

def searchbar(request):

    category = request.GET.get('category')

    category_data = ProductCategory.objects.filter(name = category)

    brand_obj = Brand.objects.filter(category_key__in = category_data)


    product_obj = ProductDetail.objects.filter(product_category__in = category_data)

    category_obj = ProductCategory.objects.all()
    add_cart_count = AddToCard.objects.filter(user_key = request.user, is_wishlist = False).count()
    add_wishlist_count = AddToCard.objects.filter(user_key = request.user, is_wishlist = True).count()



    context = {
        'product_obj':product_obj,
        'category_obj':category_obj,
        'add_cart_count':add_cart_count,
        'add_wishlist_count':add_wishlist_count,
        'brand_obj':brand_obj,
    }

    return render(request,'products.html', context)

def deletecart(request, id):

    AddToCard.objects.filter(pk = id).delete()
    return redirect('product:finalcart')

def product_detail(request, id):

    add_obj = AddToCard.objects.filter(user_key = request.user)
    product_data = ProductDetail.objects.get(pk = id)
    total = add_obj.filter(user_key = request.user,product_key = product_data).count()
    partial_count = add_obj.filter(user_key = request.user, product_key = product_data).aggregate(total_piece = Sum('product_quantity'))
    add_cart_count = add_obj.filter(user_key = request.user, is_wishlist = False).count()
    add_wishlist_count = add_obj.filter(user_key = request.user, is_wishlist = True).count()
    total_data_product = ProductDetail.objects.filter(pk = id).aggregate(total_piece = Sum('product_stock'))
    review_product = Review.objects.filter(product_key = id)

    context = {
        'review_product':review_product,
        'product_data':product_data,
        'add_cart_count':add_cart_count,
        'add_wishlist_count':add_wishlist_count,
        'total':total,
        'partial_count':partial_count,
        'total_data_product':total_data_product,
    }

    return render(request, 'single-product.html', context)

def Checkout(request):

    data_cart = AddToCard.objects.filter(user_key = request.user)

    add_cart_count = data_cart.filter(user_key = request.user, is_wishlist = False).count()
    add_wishlist_count = data_cart.filter(user_key = request.user, is_wishlist = True).count()
    add_obj = data_cart.filter(user_key = request.user, is_wishlist = False)
    city_obj = city.objects.all()
    payment_obj = PaymentMode.objects.all()

    context = {
        'add_cart_count':add_cart_count,
        'add_wishlist_count':add_wishlist_count,
        'add_obj':add_obj,
        'city_obj':city_obj,
        'payment_obj':payment_obj,
    }

    return render(request, 'checkout.html', context)

def ConfirmOrder(request):
    if request.method == "POST":
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        subtotal = request.POST['subtotal']
        quantity = request.POST.getlist('quantity')
        payment = request.POST['payment']
        email = request.POST['email']
        number = request.POST['number']
        add1 = request.POST['add1']
        add2 = request.POST['add2']
        city_data = request.POST.get('city')
        zip  = request.POST['zip']
        product = request.POST.getlist('product')

        payment_data = PaymentMode.objects.get(pk = payment)
        city_data = city.objects.get(pk = city_data)


        address = add1 + "," + add2

        for pro in product:
            product_data = AddToCard.objects.get(pk = pro)
            quantity1 = product_data.product_quantity

            product = ProductDetail.objects.get(pk = product_data.product_key.id)
            product_quantity = product.product_stock

            if int(quantity1)>int(product_quantity):
                print("you cant order"+ product.product_name)
            else:
                product_quantity = int(product_quantity) - int(quantity1)
                ProductDetail.objects.filter(pk = product_data.product_key.id).update(product_stock = product_quantity)
                Order.objects.bulk_create([
                         Order(user_key = request.user, payment_key = payment_data, quantity = product_data.product_quantity , city_key = city_data, address = address,
                         first_name = first_name, last_name = last_name, email = email, phone_number = number, zip_code = zip, total_price = subtotal,
                         product_key = product_data,
                    )
                ])

        # product_data = ProductDetail.objects.filter(pk__in = product)
        # print(product_data)
        #
        # for product in product_data:
        #     print(product.id)
        #
        # payment_data = PaymentMode.objects.get(pk = payment)
        # city_data = city.objects.get(pk = city_data)
        #
        # for product in product_data:
        #     Order.objects.bulk_create([
        #             Order(user_key = request.user, payment_key = payment_data, quantity = 1, city_key = city_data, address = address,
        #             first_name = first_name, last_name = last_name, email = email, phone_number = number, zip_code = zip, total_price = subtotal,
        #             product_key = product.id
        #         )
        #     ])



        # order_obj = Order()
        # order_obj.user_key = request.user
        # order_obj.first_name = first_name
        # order_obj.last_name = last_name
        # order_obj.total_price = subtotal
        # order_obj.email = email
        # order_obj.phone_number = number
        # order_obj.address = address
        # city_instance = city.objects.get(pk = city_data)
        # order_obj.city_key = city_instance
        # payment_instance = PaymentMode.objects.get(pk = payment)
        # order_obj.payment_key = payment_instance
        # order_obj.zip_code = zip
        # order_obj.save()
        # order_obj.product_key.set(product)



    return redirect('product:checkout')


def myorders(request):

    data_cart = AddToCard.objects.filter(user_key = request.user)
    order_obj = Order.objects.filter(user_key = request.user)
    add_cart_count = data_cart.filter(user_key = request.user, is_wishlist = False).count()
    add_wishlist_count = data_cart.filter(user_key = request.user, is_wishlist = True).count()


    context = {
        'order_obj':order_obj,
        'add_cart_count':add_cart_count,
        'add_wishlist_count':add_wishlist_count,
    }

    return render(request, 'myorders.html', context)

def searchbrand(request):

    brand = request.GET.get('brand')

    brand_data = Brand.objects.filter(name = brand)

    category = []
    for brand in brand_data:
        category.append(brand.category_key)

    brand_obj = Brand.objects.filter(category_key__in = category)

    product_obj = ProductDetail.objects.filter(product_brand__in = brand_data)

    category_obj = ProductCategory.objects.all()
    add_cart_count = AddToCard.objects.filter(user_key = request.user, is_wishlist = False).count()
    add_wishlist_count = AddToCard.objects.filter(user_key = request.user, is_wishlist = True).count()

    context = {
        'product_obj':product_obj,
        'category_obj':category_obj,
        'add_cart_count':add_cart_count,
        'add_wishlist_count':add_wishlist_count,
        'brand_obj':brand_obj,
    }

    return render(request,'products.html', context)




def delete_all_cart(request):

    if request.method == 'POST':
        cart_delete = request.POST.getlist('cart_delete')

    return redirect ('product:finalcart')

def CompareProduct(request):

    product = request.POST['product']

    product_obj = ProductDetail.objects.get(pk = product)

    if Compare.objects.filter(user_key = request.user).count() >= 2:
        data = {
            'message':'Not More than 2 products'
        }
        return JsonResponse(data)

    elif Compare.objects.filter(product_key = product_obj):
        data = {
            'message':'Already in Compare List'
        }
        return JsonResponse(data)

    else:
        compare_obj = Compare()
        compare_obj.user_key = request.user
        product_instance = ProductDetail.objects.get(pk = product)
        compare_obj.product_key = product_instance
        compare_obj.save()

    data = {
        'message': product_obj.product_name + " " +'added To Compare List',
    }
    return JsonResponse(data)

def CompareView(request):

    compare_obj = Compare.objects.filter(user_key = request.user)

    context = {
        'compare_obj':compare_obj,
    }

    return render(request, 'compare.html', context)

def rating(request, id):
    if request.method == 'POST':
        rating = request.POST['rating']
        review = request.POST['review']

        add_review = Review()
        add_review.user_key = request.user
        product_instance = ProductDetail.objects.get(pk = id)
        add_review.product_key = product_instance
        add_review.comment = review
        add_review.rating = rating
        add_review.save()

    return redirect('product:product_detail',id=id)


def tracking(request):
    if request.method == 'POST':
        order = request.POST['order']


        if Order.objects.filter(order_id__startswith = order):
            odetail = Order.objects.filter(order_id__startswith = order)
            context = {
                'odetails':odetail,
            }
            return render(request, 'tracking.html',context)
        else:
            return redirect('product:tracking')


    return redirect('product:tracking')

def delete_compare_list(request):
    if request.method == 'POST':
        compare = request.POST['compare']

        Compare.objects.filter(pk = compare).delete()


    return redirect('product:compareview')
