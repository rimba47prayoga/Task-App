from rest_framework import serializers

from .models import TaskProject


class TaskProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskProject
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
        fields = ['id', 'name', 'slug', 'board_name', 'project_type', 'created_by',
                  'created_date']
