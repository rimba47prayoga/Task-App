from django.db import models

from core.models import BaseModel


class TaskProject(BaseModel):
    name = models.CharField(max_length=100)
    project_type = models.CharField(max_length=100)
    board_name = models.CharField(max_length=10)
    logo = models.ImageField(null=True, blank=True)
    descriptions = models.TextField(null=True, blank=True)
