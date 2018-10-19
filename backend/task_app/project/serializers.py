from rest_framework import serializers

from .models import TaskProject


class TaskProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskProject
        fields = '__all__'
