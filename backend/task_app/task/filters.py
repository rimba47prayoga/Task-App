from django_filters import rest_framework as filters

from .models import Task


class TaskFilter(filters.FilterSet):
    assignee = filters.NumberFilter(field_name='assignee')

    class Meta:
        model = Task
        fields = ['assignee']
