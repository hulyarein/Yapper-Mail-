from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Fields to display in the list view of the admin
    list_display = (
        'username', 
        'first_name', 
        'middle_name', 
        'last_name', 
        'email', 
        'pnumber', 
        'birthday', 
        'gender', 
        'home_address', 
        'work_address', 
        'profile_picture',
        'is_staff', 
        'is_active',
    )
    list_filter = ('is_staff', 'is_active', 'gender')  # Add filters for admin
    search_fields = ('username', 'email', 'pnumber', 'first_name', 'last_name')

    # Fields to include in the detailed view of a user
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': (
                'middle_name', 
                'pnumber', 
                'birthday', 
                'gender', 
                'home_address', 
                'work_address', 
                'profile_picture',
            )
        }),
    )

    # Fields to include when adding a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': (
                'middle_name', 
                'pnumber', 
                'birthday', 
                'gender', 
                'home_address', 
                'work_address', 
                'profile_picture',
            ),
        }),
    )

    # Specify the fields to display when editing a user
    ordering = ('username',)