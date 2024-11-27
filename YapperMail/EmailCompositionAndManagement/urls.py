from django.urls import path
from . import views


urlpatterns = [
    path('composeEmail/<int:pk>',views.email_composition,name='email_composition'),
    path('emailSentView/<int:pk>/<int:ok>',views.email_sent_view,name='emailSentView'),
    path('emailReceiveView/',views.email_reply_view,name='emailReceiveView'),
    path('editEmail/<int:pk>/<int:uk>',views.edit_email,name='editEmail'),
    path('editReply/<int:pk>/<int:uk>',views.edit_reply,name='editReply'),
    path('download/<path:filename>/', views.download_file, name='download_fileme'),
    path('changeImage/<int:pk>',views.editExistingImage,name = "editExistingImage"),
    path('changeImageReply/<int:pk>',views.existingReplyFile,name = "existingReplyFile"),
    path('emailList',views.emailListView,name='emailListView'),
    path('emailList/sent',views.sentEmailList,name = "sentEmailList"),
    path('deleteEmail',views.deleteEmailFunc,name = "deleteEmailFunc"),
    path('deleteReply',views.deleteReplyFunc,name = "deleteReplyFunc")
]