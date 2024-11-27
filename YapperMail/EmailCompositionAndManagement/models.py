from django.db import models
from django.contrib.auth.models import User
from landing.models import *
# Create your models here.

class TemporaryUser(models.Model):
    
    userEmail = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.userEmail}"
    

class Email(models.Model):
    fromUser = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='sent_emails',null=True)
    toUser = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='receive_emails',null=True)
    subject = models.CharField(max_length=500)
    content = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    isDeleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject}"
    


class EmailFiles(models.Model):
    fromUser = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='sent_emailFiles',null=True)
    toUser = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='receive_emailFiles',null=True)
    emailId = models.ForeignKey(Email,on_delete=models.CASCADE,null=True)
    file = models.FileField(upload_to='uploads/')


    def __str__(self):
        return f"{self.file}"
    

class Reply(models.Model):
    fromUser = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="reply_to_email",null=True)
    emailId = models.ForeignKey(Email,on_delete=models.CASCADE,related_name="emialReply",null=True)
    content = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)   

    def __str__(self):
        return f"{self.id}-{self.fromUser}"
    

class ReplyFiles(models.Model):
    fromUser = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="reply_files_user",null=True)
    emailId = models.ForeignKey(Email,on_delete=models.CASCADE,related_name="emialReplyFiles",null=True,blank=True)
    replyid = models.ForeignKey(Reply,on_delete=models.CASCADE,related_name="reply_file_replyid",null=True)
    file = models.FileField(upload_to='uploads/')

    def __str__(self):
        return f"{self.id}-{self.file}"

    

