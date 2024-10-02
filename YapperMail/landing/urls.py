from django.urls import path, include
from . import views
from .views import signupForm, loginForm

urlpatterns = [
    path('', views.landing, name='landing'), 
    path('signup', views.signupForm, name="signup"),
    path('login', views.loginForm, name="login"),
    path('home', views.home, name="home"),
    path("accounts/", include("django.contrib.auth.urls")),  

    
]