from django.urls import path
from . import views


urlpatterns = [
    path('composeEmail/',views.email_composition,name='email_composition'),
    path('emailSentView/',views.email_sent_view,name='emailSentView'),
    path('emailReceiveView/',views.email_sent_view,name='emailReceiveView'),
    path('editEmail/',views.edit_email,name='editEmail'),
    path('editReply/',views.edit_reply,name='editReply'),
]