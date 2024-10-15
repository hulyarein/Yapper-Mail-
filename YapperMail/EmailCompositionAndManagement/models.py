from django.db import models

# Create your models here.

class TemporaryUser(models.Model):
    userEmail = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.userEmail}"
    

class Email(models.Model):
    fromUser = models.ForeignKey(TemporaryUser,on_delete=models.CASCADE,related_name='sent_emails')
    toUser = models.ForeignKey(TemporaryUser,on_delete=models.CASCADE,related_name='receive_emails')
    subject = models.CharField(max_length=500)
    content = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject}"
    


class EmailFiles(models.Model):
    fromUser = models.ForeignKey(TemporaryUser,on_delete=models.CASCADE,related_name='sent_emailFiles')
    toUser = models.ForeignKey(TemporaryUser,on_delete=models.CASCADE,related_name='receive_emailFiles')
    emailId = models.ForeignKey(Email,on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')


    def __str__(self):
        return f"{self.file}"
    

class Reply(models.Model):
    fromUser = models.ForeignKey(TemporaryUser,on_delete=models.CASCADE,related_name="reply_to_email")
    emailId = models.ForeignKey(Email,on_delete=models.CASCADE,related_name="emialReply")
    content = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)   

    def __str__(self):
        return f"{self.id}-{self.fromUser}"
    

class ReplyFiles(models.Model):
    fromUser = models.ForeignKey(TemporaryUser,on_delete=models.CASCADE,related_name="reply_files_user")
    emailId = models.ForeignKey(Email,on_delete=models.CASCADE,related_name="emialReplyFiles",null=True,blank=True)
    replyid = models.ForeignKey(Reply,on_delete=models.CASCADE,related_name="reply_file_replyid")
    file = models.FileField(upload_to='uploads/')

    def __str__(self):
        return f"{self.id}-{self.file}"

    

