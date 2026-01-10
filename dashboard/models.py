from django.db import models
"""
import uuid
from django.db import models
#hada radi ikon lcore dyal app
from accounts.models import Owner,Director
class Organization(models.Model):
    org_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

class Center(models.Model):
    center_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    director = models.OneToOneField(Director, on_delete=models.SET_NULL, null=True)

class Room(models.Model):
    room_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    center = models.ForeignKey(Center, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    fire_capacity = models.IntegerField()

class Group(models.Model):
    group_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    center = models.ForeignKey(Center, on_delete=models.CASCADE)
    ratio_category = models.CharField(max_length=50) # 'UNDER_24M', etc.
    
    # Real-time Stats (Calculated fields)
    current_total_points = models.IntegerField(default=0)
    is_compliant = models.BooleanField(default=True)
    """
