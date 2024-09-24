from django.urls import path
from . import views

urlpatterns = [
    path('', views.profilePage,name='profile'),
    path('profilePage/', views.profilePage, name='profile')
]
