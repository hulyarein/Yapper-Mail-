from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    pnumber = models.CharField(max_length=13, unique=True)  # Add pnumber field
    middle_name = models.CharField(max_length=30, default=' ', blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=50, default='PNS')
    home_address = models.CharField(max_length=200, blank=True, null=True)
    work_address = models.CharField(max_length=200, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True,default='images/default_profile.jpg')

    def __str__(self):
        return self.username
  
class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    pnumber = models.CharField(max_length=12)  
    fname = models.CharField(max_length=30, default='First Name')
    lname = models.CharField(max_length=30, default='Last Name')
    email = models.EmailField(default='example@example.com')

    def __str__(self):
        return self.user.usernam