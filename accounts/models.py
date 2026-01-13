from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role_type = models.CharField(max_length=20, choices=[
        ('owner', 'Owner'), ('director', 'Director'), 
        ('vice_director', 'Vice Director'), ('educator', 'Educator'), ('parent', 'Parent')
    ])
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    full_name = models.CharField(max_length=255)

class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    office_address = models.TextField()

class Director(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    qualification_cert = models.CharField(max_length=255)
    hired_at = models.DateField()
    
   
    organization = models.ForeignKey('dashboard.Organization', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.full_name

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    home_address = models.TextField()
    billing_reference = models.CharField(max_length=100)
class Educator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # n-linkiw Educator m3a l-Director li ghadi y-manage-ih
    manager = models.ForeignKey(Director, on_delete=models.SET_NULL, null=True, related_name='educators')
    # n-linkiw Educator m3a l-Center fin khdam
    center = models.ForeignKey('dashboard.Center', on_delete=models.CASCADE, related_name='staff')
    
    specialization = models.CharField(max_length=100, blank=True)
    hired_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} - Educator"