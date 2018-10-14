from datetime import datetime

from django.db import models


class BaseModelQueryset(models.QuerySet):

    def delete(self):
        return self.update(
            deleted=True,
            deleted_time=datetime.now()
        )

    def active(self):
        return self.filter(is_deleted=False)

    def deleted(self):
        return self.filter(is_deleted=False)


class BaseModelManager(models.Manager):

    def get_queryset(self):
        return BaseModelQueryset(self.model, using=self._db).active()
