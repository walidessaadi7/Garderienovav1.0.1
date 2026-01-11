from django.contrib import admin
from .models import Organization, Center, Room, Group
from django.contrib import admin
from .models import Owner, Director

admin.site.register(Owner)
admin.site.register(Director)
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'org_id', 'owner')
    search_fields = ('name',)

@admin.register(Center)
class CenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'center_id', 'org', 'director')
    list_filter = ('org',)
    search_fields = ('name',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'room_id', 'center', 'fire_capacity')
    list_filter = ('center',)
    search_fields = ('name',)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('group_id', 'center', 'room', 'ratio_category', 'current_total_points', 'is_compliant')
    list_filter = ('center', 'is_compliant', 'ratio_category')
    # هادي كتعاونك تشوف الـ Groups اللي فيهم مشكل بسرعة
    list_editable = ('is_compliant',)