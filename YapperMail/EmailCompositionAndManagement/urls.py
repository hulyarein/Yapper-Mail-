from django.urls import path
from . import views


urlpatterns = [
    path('composeEmail/',views.email_composition,name='email_composition'),
    path('emailSentView/',views.email_sent_view,name='emailSentView'),
    path('emailReceiveView/',views.email_reply_view,name='emailReceiveView'),
    path('editEmail/<int:pk>',views.edit_email,name='editEmail'),
    path('editReply/<int:pk>',views.edit_reply,name='editReply'),
    path('download/<path:filename>/', views.download_file, name='download_file'),
    path('changeImage/<int:pk>',views.editExistingImage,name = "editExistingImage"),
    path('changeImageReply/<int:pk>',views.existingReplyFile,name = "existingReplyFile"),
]