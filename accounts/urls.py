from django.urls import path

from .views import login, register, home, logout

app_name = 'accounts'

urlpatterns = [
    path('Login/', login, name='login'),
    path('Register/', register, name ='register'),
    path('home/', home, name = 'home'),
    path('logout/', logout, name ='logout'),
]
