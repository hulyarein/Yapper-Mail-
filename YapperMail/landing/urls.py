from django.urls import path, include
from . import views
from .views import signupForm, loginForm

urlpatterns = [
    path('', views.landing, name='landing'), 
    path('signup/', views.signupForm, name="signup"),
    path('login/', views.loginForm, name="login"),
    path('enternumber/', views.enterpnumber, name="enternumber"),
    path('send-otp/', views.send_otp, name='send_otp'),
    path('home/', views.home, name="home"),
    path('email-list/', views.email_list, name="email_list"),
    path('verify-otp/', views.verify_otp, name='verify_otp'),       
    path('profile/', views.profile, name='myprofile'),  
    path('EmailComposition/', include('EmailCompositionAndManagement.urls')), 
    path('UserProfile/', include('UserProfile.urls')), 
    path('reset-password/', views.reset_password, name='reset_password'),
    path("accounts/", include("django.contrib.auth.urls")),  
]