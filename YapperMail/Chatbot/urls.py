from django.urls import path
from . import views


urlpatterns = [
    path('chatbotsystem/',views.show_promt_Disp,name='show_promt_Disp'),
    path('chatbotsystem/pass/',views.send_message,name = "send_message"),
]
