from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    created_by = models.ForeignKey(User)
    created_date = models.DateTimeField(auto_now_add=True)

    is_deleted = models.BooleanField(default=False)
    deleted_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
