from django.db import models


class TaskManager(models.Manager):
    def get_queryset(self):
        return super(TaskManager, self).get_queryset().filter(is_deleted=False)
