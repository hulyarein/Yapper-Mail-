from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Fields to display in the list view of the admin
    list_display = ('username', 'first_name', 'last_name', 'email', 'pnumber')
    
    # Fields to include in the detailed view of a user
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('pnumber',)}),
    )
    
    # Fields to include when adding a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('first_name', 'last_name', 'email', 'pnumber')}),
    )
admin.site.register(Profile)

