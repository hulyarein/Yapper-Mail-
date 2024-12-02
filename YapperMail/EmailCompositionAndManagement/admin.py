from django.contrib import admin
from .models import Email,EmailFiles,Reply,ReplyFiles,CategoryEmail

# Register your models here.
admin.site.register(Email)
admin.site.register(EmailFiles)
# admin.site.register(TemporaryUser)
admin.site.register(Reply)
admin.site.register(ReplyFiles)
admin.site.register(CategoryEmail)

