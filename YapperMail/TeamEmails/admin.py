from django.contrib import admin

from .models import TeamEmail,TeamEmailFiles,TeamReply,TeamReplyFiles

# Register your models here.
admin.site.register(TeamEmail)
admin.site.register(TeamEmailFiles)
admin.site.register(TeamReply)
admin.site.register(TeamReplyFiles)
