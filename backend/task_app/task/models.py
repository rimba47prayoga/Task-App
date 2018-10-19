from django.contrib.auth.models import User
from django.db import models
from django.utils.functional import cached_property

from core.models import BaseModel
from project.models import TaskProject
from .choices import TaskChoices
from .managers import TaskManager


class Task(BaseModel):
    project = models.ForeignKey(TaskProject, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    task_type = models.IntegerField(
        choices=TaskChoices.TASK_TYPE_CHOICES,
        default=TaskChoices.TASK
    )
    label = models.CharField(max_length=255, null=True, blank=True)
    priority = models.IntegerField(choices=TaskChoices.PRIORITY_CHOICES)
    branch = models.CharField(max_length=10, unique=True)
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

    deadline = models.DateTimeField()
    descriptions = models.TextField(null=True, blank=True)
    
    objects = TaskManager()

    def __str__(self):
        return self.title

    @cached_property
    def branch_name(self):
        return self.project.board_name + '-' + self.branch

    @classmethod
    def generate_branch(cls):
        last_branch = cls.objects.only('branch').last()
        if not last_branch:
            return str(1).zfill(4)
        return str(int(last_branch.branch) + 1).zfill(4)
