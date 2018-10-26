from django_filters import rest_framework as filters

from .models import Task


class TaskFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name='id')
    project = filters.NumberFilter(field_name='project')
    assignee = filters.NumberFilter(field_name='assignee')

    class Meta:
        model = Task
        fields = ['assignee']
