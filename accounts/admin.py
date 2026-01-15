from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Owner, Director, Parent, Educator  # Import all your models

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'full_name', 'role_type', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('role_type', 'full_name', 'phone_number')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Info', {'fields': ('role_type', 'full_name', 'phone_number')}),
    )

# Register the Custom User
admin.site.register(User, CustomUserAdmin)

# Register the Profile Models so they appear in Admin


admin.site.register(Parent)
admin.site.register(Educator)