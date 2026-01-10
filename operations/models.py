##
"""
from django.db import models
import uuid
from dashboard.models import Center,Group
class Child(models.Model):
    child_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    center = models.ForeignKey(Center, on_delete=models.CASCADE)
    assigned_group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=100)
    current_ratio_weight = models.IntegerField() 
    medical_info = models.JSONField(default=dict)

class AttendanceLog(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(null=True)
    check_out_time = models.DateTimeField(null=True)
    ratio_weight_snapshot = models.IntegerField()
 """
