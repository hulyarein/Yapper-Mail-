from django.db import models
# from django.contrib.auth.models import User
from landing.models import CustomUser as User

# Create your models here.

class TeamEmail(models.Model):
    fromUser = models.ForeignKey(User,on_delete=models.CASCADE,related_name='team_sent_emails',null=True)
    adminUsers = models.ManyToManyField(User, related_name="team_admin_Users")
    memberUsers = models.ManyToManyField(User, related_name="team_member_Users")
    subject = models.CharField(max_length=500)
    content = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    isDeleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject}"
    


class TeamEmailFiles(models.Model):
    emailId = models.ForeignKey(TeamEmail,on_delete=models.CASCADE,null=True)
    file = models.FileField(upload_to='uploads/')


    def __str__(self):
        return f"{self.file}"
    

class TeamReply(models.Model):
    fromUser = models.ForeignKey(User,on_delete=models.CASCADE,related_name="team_reply_to_email",null=True)
    emailId = models.ForeignKey(TeamEmail,on_delete=models.CASCADE,related_name="team_emialReply",null=True)
    content = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)   

    def __str__(self):
        return f"{self.id}-{self.fromUser}"
    

class TeamReplyFiles(models.Model):
    fromUser = models.ForeignKey(User,on_delete=models.CASCADE,related_name="team_reply_files_user",null=True)
    emailId = models.ForeignKey(TeamEmail,on_delete=models.CASCADE,related_name="team_emialReplyFiles",null=True,blank=True)
    replyid = models.ForeignKey(TeamReply,on_delete=models.CASCADE,related_name="team_reply_file_replyid",null=True)
    file = models.FileField(upload_to='uploads/')

    def __str__(self):
        return f"{self.id}-{self.file}"
    

class CategoryTeamEmail(models.Model):
    fromUser = models.ForeignKey(User,on_delete=models.CASCADE,related_name="team_category_user",null=True)
    emaildCat= models.ForeignKey(TeamEmail,on_delete=models.CASCADE,related_name="teamcatgEmail",null=True)
    isDelegate = models.BooleanField(default = False)
    isScheduled = models.BooleanField(default = False)
    isDo = models.BooleanField(default = False)
    
