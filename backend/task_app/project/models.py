from django.db import models
from django_extensions.db.fields import AutoSlugField

from core.models import BaseModel


class TaskProject(BaseModel):
    SOFTWARE, WEB_SERVICES = range(2)
    PROJECT_TYPE_CHOICES = (
        (SOFTWARE, 'Software Project'),
        (WEB_SERVICES, 'Web Services Project')
    )
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name')
    project_type = models.IntegerField(choices=PROJECT_TYPE_CHOICES)
    board_name = models.CharField(max_length=10)
    logo = models.ImageField(null=True, blank=True)
    descriptions = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
