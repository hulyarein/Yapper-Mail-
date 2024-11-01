# from django.contrib.auth.models import AbstractUser, Group, Permission
# from django.db import models
# from phonenumber_field.modelfields import PhoneNumberField

# class User(AbstractUser):
#     middle_name = models.CharField(max_length=50, blank=True, null=True)
#     phone_number = PhoneNumberField(unique=True)
#     birthday = models.DateField(blank=True, null=True)
#     gender = models.CharField(max_length=50, blank=True, null=True)
#     email_address = models.EmailField(max_length=254, unique=True)
#     home_address = models.CharField(max_length=200, blank=True, null=True)
#     work_address = models.CharField(max_length=200, blank=True, null=True)

#     groups = models.ManyToManyField(
#         Group,
#         related_name='custom_user_groups',
#         blank=True
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         related_name='custom_user_permissions',
#         blank=True
#     )

#     def __str__(self):
#         return self.username

