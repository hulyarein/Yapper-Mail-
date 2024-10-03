from django.urls import path
from . import views

urlpatterns = [
    path('profilePage/', views.profilePage, name='profile'),
    path('profilePage/PersonalInfo/Name/', views.changeName, name='changeName'),
    path('profilePage/PersonalInfo/Birthday', views.changeBday, name='changeBday'),
    path('profilePage/PersonalInfo/Gender', views.changeGender, name='changeGender'),
    path('profilePage/ContactInfo/Number', views.changeNumber, name='changeNumber'),
    path('profilePage/ContactInfo/EmailAddress', views.changeEmail, name='changeEmail'),
    path('profilePage/Addresses/Home', views.changeHome, name='changeHome'),
    path('profilePage/Addresses/Work', views.changeWork, name='changeWork'),
]
