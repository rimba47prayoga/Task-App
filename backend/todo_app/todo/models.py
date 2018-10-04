from django.db import models
from core.models import BaseModel


class Todo(BaseModel):
    title = models.CharField(max_length=255)
    descriptions = models.TextField()
