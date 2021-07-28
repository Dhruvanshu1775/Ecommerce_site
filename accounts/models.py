from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserInfo(models.Model):
    user_key    = models.OneToOneField(User,on_delete = models.CASCADE)
    is_customer = models.BooleanField(default = False)
    is_seller   = models.BooleanField(default = False)

    def __str__(self):
        return str(self.user_key)
