from django.contrib import admin
from .models import Email,EmailFiles,TemporaryUser

# Register your models here.
admin.site.register(Email)
admin.site.register(EmailFiles)
admin.site.register(TemporaryUser)
