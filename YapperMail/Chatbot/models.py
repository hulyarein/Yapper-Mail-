from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ChatPropmt(models.Model):
    fromUser = models.ForeignKey(User,on_delete=models.CASCADE,related_name='promt_user')
    prompt_text = models.CharField(max_length=1000)
    fromAi = models.BooleanField(default=False)

    def __str__(self):
        return f" chat {self.fromUser} {self.id}"
