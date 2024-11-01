from django.db import models
from django.contrib.auth.models import User,AbstractUser
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date, timedelta
import uuid
from django.utils import timezone

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=50) 
    pnumber = PhoneNumberField(unique=True)
    birthday = models.DateField(default=date(2000,1,1))
    gender = models.CharField(max_length=50, default='PNS')
    email_address = models.EmailField(max_length=254, unique=True)
    home_address = models.CharField(max_length=200, blank=True, null=True)
    work_address = models.CharField(max_length=200, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True,default='default_profile.jpg')

    def __str__(self):
        return self.user.username
    
    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)

    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()

# Abstracted User pero kapoy change sa whole shit :((
# class User(AbstractUser):
#     middle_name = models.CharField(max_length=50) 
#     pnumber = PhoneNumberField(unique=True)
#     birthday = models.DateField(default=date(2000,1,1))
#     gender = models.CharField(max_length=50, blank=True, null=True)
#     email_address = models.EmailField(max_length=254, unique=True)
#     home_address = models.CharField(max_length=200, blank=True, null=True)
#     work_address = models.CharField(max_length=200, blank=True, null=True)
#     profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True,default='default_profile.jpg')

#     groups = models.ManyToManyField(
#         'auth.Group',
#         related_name='profile_groups',
#         blank=True
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         related_name='profile_user_permissions',
#         blank=True
#     )

#     def __str__(self):
#         return self.user.username