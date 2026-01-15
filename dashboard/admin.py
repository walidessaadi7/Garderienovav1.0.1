from django.contrib import admin
from .models import Organization, Center, Room, Group,Child  # Make sure this is your dashboard models
from accounts.models import Owner, Director  # Import from accounts app

# -------------------------------
# Register Owner and Director
# -------------------------------
admin.site.register(Owner)
admin.site.register(Director)

# -------------------------------
# Organization Admin
# -------------------------------
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'org_id', 'owner')
    search_fields = ('name', 'owner__username')  # assuming Owner has username/email

# -------------------------------
# Center Admin
# -------------------------------
@admin.register(Center)
class CenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'center_id', 'org', 'director')
    list_filter = ('org',)
    search_fields = ('name', 'director__user__username')  # assuming Director linked to User

# -------------------------------
# Room Admin
# -------------------------------
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'room_id', 'center', 'fire_capacity')
    list_filter = ('center',)
    search_fields = ('name',)

# -------------------------------
# Group Admin
# -------------------------------
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('group_id', 'center', 'room', 'ratio_category', 'current_total_points', 'is_compliant')
    list_filter = ('center', 'is_compliant', 'ratio_category')
    list_editable = ('is_compliant',)

@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'parent', 'center', 'birth_date', 'gender', 'created_at')
    list_filter = ('center', 'gender')
    search_fields = ('first_name', 'last_name', 'parent__user__full_name', 'center__name')