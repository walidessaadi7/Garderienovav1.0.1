from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # Hna kankhtarou chno i-ban f l-lixta dyal les users
    list_display = ('username', 'email', 'full_name', 'role_type', 'is_staff')
    
    # Hna chno i-ban mli t-clicki 3la user bach t-modifihi
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('role_type', 'full_name', 'phone_number')}),
    )
    
    # Hna chno i-ban mli t-creer user jdid men l-admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Info', {'fields': ('role_type', 'full_name', 'phone_number')}),
    )

# Darori t-registri l-model dyalk
admin.site.register(User, CustomUserAdmin)