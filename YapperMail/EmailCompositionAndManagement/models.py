from django.db import models

# Create your models here.
class Email(models.Model):
    fromUser = models.CharField(max_length = 100)
    toUser = models.CharField(max_length= 100)
    subject = models.CharField(max_length=500)
    content = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fromUser
    


class EmailFiles(models.Model):
    fromUser = models.CharField(max_length = 100)
    toUser = models.CharField(max_length= 100)
    emailId = models.ForeignKey(Email,on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')


    def __str__(self):
        return self.fromUser
    
    
