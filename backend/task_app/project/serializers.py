from rest_framework import serializers

from .models import TaskProject


class TaskProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskProject
        fields = ['id', 'name', 'board_name', 'project_type', 'created_by',
                  'created_date']
