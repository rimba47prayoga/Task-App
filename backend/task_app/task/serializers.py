from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Task


class AssigneeSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        if hasattr(obj, 'userprofile'):
            return obj.userprofile.avatar
        return None

    class Meta:
        model = User
        fields = ['username', 'avatar']


class TaskSerializer(serializers.ModelSerializer):
    assignee = AssigneeSerializer()

    class Meta:
        model = Task
        fields = '__all__'
