from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from .models import UserInfo
from product.models import AddToCard
# Create your views here.

def register(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            data = {
            'username':username,
            'email':email,
            'message':'reenter password'
            }
            return render(request,'register.html',data)
        elif User.objects.filter(username = username):
            data = {
            'username':username,
            'email':email,
            'message':'Username Already Exist'
            }
            return render(request,'register.html',data)
        else:
            user1 = User.objects.create_user(username = username, password = password, email = email)

            user_obj = UserInfo()
            user_obj.user_key = user1
            user_obj.is_customer = True
            user_obj.save()

            auth.login(request, user1)
            return redirect('accounts:home')

    return render(request, 'register.html')

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user1 = auth.authenticate(username = username, password = password)
        if user1 is not None:
            auth.login(request, user1)
            if user1.userinfo.is_customer:
                return redirect('accounts:home')
            else:
                print("admin")
        else:
            return redirect('accounts:login')

    return render(request, 'login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)

    return redirect('accounts:login')

def home(request):

    add_cart_count = AddToCard.objects.filter(user_key = request.user, is_wishlist = False).count()
    add_wishlist_count = AddToCard.objects.filter(user_key = request.user, is_wishlist = True).count()


    context = {
        'add_cart_count':add_cart_count,
        'add_wishlist_count':add_wishlist_count,
    }

    return render(request,'home.html', context)
