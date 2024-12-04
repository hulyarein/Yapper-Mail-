from django.urls import path
from . import views

urlpatterns = [
    path('profilePage/', views.profilePage, name='profile'),
    path('profilePage/Name/', views.changeName, name='changeName'),
    path('profilePage/Birthday', views.changeBday, name='changeBday'),
    path('profilePage/Gender', views.changeGender, name='changeGender'),
    path('profilePage/Number', views.changeNumber, name='changeNumber'),
    path('profilePage/Home', views.changeHome, name='changeHome'),
    path('profilePage/Work', views.changeWork, name='changeWork'),
    path('profilePage/Password', views.changePassword, name='changePassword'),
    path('logout', views.logout_user, name='logout')
]


