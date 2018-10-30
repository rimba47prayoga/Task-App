from django.contrib.auth.models import User
from django.db import models

from core.models import BaseModel
from .choices import *


class Notifications(BaseModel):
    notification_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, related_name='recipients', on_delete=models.CASCADE)
    subject = models.PositiveSmallIntegerField(
        choices=SUBJECT_CHOICES,
        default=ASSIGNEE_TASK
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_by = None

    def __str__(self):
        return self.title

    @classmethod
    def generate_notification_id(cls, user_id, subject, branch_name=None):
        if isinstance(subject, list):
            subject = "".join([str(i) for i in subject])
        result = f"NF-U{user_id}-S{subject}"
        if branch_name:
            result += f"-B{branch_name}"
        return result
