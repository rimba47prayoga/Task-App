from django.contrib.auth.models import User
from django.db import models

from core.models import BaseModel
from .choices import TaskChoices
from .managers import TaskManager


class Task(BaseModel):

    title = models.CharField(max_length=255)
    task_type = models.IntegerField(
        choices=TaskChoices.TASK_TYPE_CHOICES,
        default=TaskChoices.TASK
    )
    label = models.CharField(max_length=255, null=True, blank=True)
    priority = models.IntegerField(choices=TaskChoices.PRIORITY_CHOICES)
    branch = models.CharField(max_length=20, unique=True)
    assignee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='assignee'
    )
    progress = models.IntegerField(
        choices=TaskChoices.PROGRESS_CHOICES,
        default=TaskChoices.TODO
    )
    
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    descriptions = models.TextField()
    
    objects = TaskManager()

    def __str__(self):
        return self.title
