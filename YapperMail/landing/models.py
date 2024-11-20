from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    pnumber = models.CharField(max_length=13, unique=True)  # Add pnumber field

    def __str__(self):
        return self.username
  
class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    pnumber = models.CharField(max_length=12)  
    fname = models.CharField(max_length=30, default='First Name')
    lname = models.CharField(max_length=30, default='Last Name')
    email = models.EmailField(default='example@example.com')

    def __str__(self):
        return self.user.username