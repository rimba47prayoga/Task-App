from django.contrib.auth.models import User
from django.db import models

from .managers import BaseModelManager


class BaseModel(models.Model):
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_created_by'
    )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='%(class)s_modified_by'
    )
    modified_date = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False)
    deleted_time = models.DateTimeField(null=True, blank=True)
    
    objects = BaseModelManager()
    objects_ori = models.Manager()

    class Meta:
        abstract = True
