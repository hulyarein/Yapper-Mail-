from django.urls import path, include
from . import views
from .views import signupForm, loginForm
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.landing, name='landing'), 
    path('signup/', views.signupForm, name="signup"),
    path('login/', views.loginForm, name="login"),
    path('home/', views.home, name="home"),
    path("accounts/", include("django.contrib.auth.urls")),  

    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)