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
    def __str__(self):
        return self.user.full_name

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    home_address = models.TextField()
    billing_reference = models.CharField(max_length=100)