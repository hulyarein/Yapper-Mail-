from django.urls import path, include
from . import views
from .views import signupForm, loginForm
from django.conf.urls.static import static
from django.conf import settings
from notifications_app.views import index
from EmailCompositionAndManagement.views import *

urlpatterns = [
    path('', views.landing, name='landing'), 
    path('signup/', views.signupForm, name="signup"),
    path('login/', views.loginForm, name="login"),
    path('enternumber/', views.enterpnumber, name="enternumber"),
    path('signinnumber/', views.signin_number, name="signin_number"),
    path('phonelogin/', views.phone_login, name="phone-login"),
    path('send-otp/', views.send_otp, name='send_otp'),
    path('home/', views.home, name="home"),
    path('email-list/', views.email_list, name="email_list"),    
    path('profile/', views.profile, name='myprofile'),  
    path('compose/<int:pk>/', index, name='compose_email'),  
    path('EmailComposition/', include('EmailCompositionAndManagement.urls')), 
    path('UserProfile/', include('UserProfile.urls')), 
    path('reset-password/', views.reset_password, name='reset_password'),
    path("accounts/", include("django.contrib.auth.urls")),  
    path('email_view/', views.email_view, name='email_view'),
    path('receive_view/', views.receive_view, name='receive_view'),
    path('retrieve_email_view/', views.retrieve_email_view, name='retrieve_email_view'),
    path('email_calendar/', views.email_calendar, name='email_calendar'),
    path('search/', views.search_emails, name='search_emails'),
    
    # static(settings.MEDIA_URL)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
