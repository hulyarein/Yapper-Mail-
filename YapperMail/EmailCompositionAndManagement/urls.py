from django.urls import path
from . import views


urlpatterns = [
    path('composeEmail/',views.email_composition,name='composeEmail')
]