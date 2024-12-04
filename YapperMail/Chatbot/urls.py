from django.urls import path
from . import views


urlpatterns = [
    path('chatbotsystem/',views.show_promt_Disp,name='show_promt_Disp'),
    path('chatbotsystem/pass/',views.send_message,name = "send_message"),
    path('chatbotdel/',views.delete_message,name = "delete_message"),
    path('chatbotdelall/',views.clear_chat,name = "clear_chat"),
]
