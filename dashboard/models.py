from typing import Any
from django.db import models

import uuid
from django.db import models
#hada radi ikon lcore dyal app
from accounts.models import Owner,Director
class Organization(models.Model):
    org_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    owner = models.OneToOneField(
        "accounts.Owner", on_delete=models.PROTECT, related_name="owned_organization"
    )
    def __str__(self):
     return self.name

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
    def __str__(self):
        return self.name
    

class Group(models.Model):
    group_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    center = models.ForeignKey(Center, on_delete=models.CASCADE)
    ratio_category = models.CharField(max_length=50) # 'UNDER_24M', etc.
    
    # Real-time Stats (Calculated fields)
    current_total_points = models.IntegerField(default=0)
    is_compliant = models.BooleanField(default=True)
class Child(models.Model):
    # Unique ID for each child
    child_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Link to Center (same app)
    center = models.ForeignKey(
        "dashboard.Center",
        on_delete=models.CASCADE,
        related_name="children"
    )

    # Link to Parent (accounts app) → use string reference
    parent = models.ForeignKey(
        "accounts.Parent",
        on_delete=models.CASCADE,
        related_name="children"
    )

    # Child info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    gender = models.CharField(max_length=10, choices=[("M", "Male"), ("F", "Female")])

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Child"
        verbose_name_plural = "Children"
        ordering = ["first_name", "last_name"] 
