from django.urls import path
from . import views
from EmailCompositionAndManagement.views import email_reply_view

urlpatterns = [
    path('index/<int:pk>', views.index, name="index"),
    path('get_user_id/', views.get_user_id, name='get_user_id'),
    path('get_logged_in/', views.get_logged_in, name='get_logged_in'),
    
]