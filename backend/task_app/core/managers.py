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

    @property
    def __queryset(self):
        return BaseModelQueryset(model=self.model, using=self._db)

    def get_queryset(self):
        return self.__queryset.active()

    def get(self, **kwargs):
        return self.get_queryset().get(**kwargs)

    def filter(self, **kwargs):
        return self.get_queryset().filter(**kwargs)

    def all(self):
        return self.get_queryset()
