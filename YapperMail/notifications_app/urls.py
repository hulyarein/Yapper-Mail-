from django.urls import path
from . import views
from EmailCompositionAndManagement.views import email_reply_view

urlpatterns = [
    path('index/<int:pk>', views.index, name="index"),
    path('get_user_id/', views.get_user_id, name='get_user_id'),
    path('get_logged_in/', views.get_logged_in, name='get_logged_in'),
    path('get_notifications/', views.get_notifications, name='get_notifications'),
    path('mark_as_read/', views.mark_as_read, name='mark_as_read'),
    path('notification_detail/<int:email_id>', views.notification_detail, name='notification_detail'),
]