# models.py
from django.db import models
from landing.models import CustomUser
from EmailCompositionAndManagement.models import *

class Notification(models.Model):
    title = models.CharField(max_length=255)  # Subject or title of the notification
    message = models.TextField()  # Content of the notification
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='from_user_notification', null=True)
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='to_user_notification', null=True)
    is_read = models.BooleanField(default=False)  # For unread/read tracking
    email_id = models.ForeignKey(Email, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
