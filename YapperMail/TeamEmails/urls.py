from django.urls import path
from . import views


urlpatterns = [
    path('composeEmail/<int:pk>',views.team_email_composition,name='team_email_composition'), 
    path('composeEmaildetails',views.compose_email_details,name = "compose_email_details"),
    path('emailList',views.team_emailListView,name='team_emailListView'),
    path('emailList/sent',views.team_sentEmailList,name = "team_sentEmailList"),
    path('emailSentView/<int:pk>/<int:ok>',views.team_email_sent_view,name='team_emailSentView'),
    path('download/<path:filename>/', views.team_download_file, name='download_file'),
    path('editEmail/<int:pk>/<int:uk>',views.team_edit_email,name='team_editEmail'),
    path('changeImage/<int:pk>',views.team_editExistingImage,name = "team_editExistingImage"),
    path('editReply/<int:pk>/<int:uk>',views.team_edit_reply,name='team_editReply'),
    path('changeImageReply/<int:pk>',views.team_existingReplyFile,name = "team_existingReplyFile"),
    path('deleteReply',views.teams_deleteReplyFunc,name = "team_deleteReplyFunc"),
    path('deleteEmail',views.team_deleteEmailFunc,name = "team_deleteEmailFunc"),
    path('removeMember/<int:pk>',views.team_removeAccessMember,name = "team_removeAccessMember"),
    path('removeAdmin/<int:pk>',views.team_removeAccessAdmin,name = "team_removeAccessAdmin"),
    path('addAdmin/<int:pk>',views.team_addAdmin,name = "team_addAdmin"),
    path('downgradeMember/<int:pk>',views.team_downgradeMember,name = "team_downgradeMember"),
    path('addCollab/<int:pk>',views.team_addCollaborator,name = "team_addCollaborator")
]


'''path('emailSentView/<int:pk>/<int:ok>',views.email_sent_view,name='emailSentView'),
    path('emailReceiveView/',views.email_reply_view,name='emailReceiveView'),
    path('editEmail/<int:pk>/<int:uk>',views.edit_email,name='editEmail'),
    path('editReply/<int:pk>/<int:uk>',views.edit_reply,name='editReply'),
    path('download/<path:filename>/', views.download_file, name='download_file'),
    path('changeImage/<int:pk>',views.editExistingImage,name = "editExistingImage"),
    path('changeImageReply/<int:pk>',views.existingReplyFile,name = "existingReplyFile"),
    path('emailList',views.emailListView,name='emailListView'),
    path('emailList/sent',views.sentEmailList,name = "sentEmailList"),
    path('deleteEmail',views.deleteEmailFunc,name = "deleteEmailFunc"),
    path('deleteReply',views.deleteReplyFunc,name = "deleteReplyFunc")
    
    
    
    '''
