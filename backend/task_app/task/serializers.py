from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Task


class SimpleUserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        if hasattr(obj, 'userprofile'):
            return obj.userprofile.avatar
        return None

    class Meta:
        model = User
        fields = ['username', 'avatar']


class TaskSerializer(serializers.ModelSerializer):
    assignee = SimpleUserSerializer(allow_null=True)
    created_by = SimpleUserSerializer(allow_null=True, required=False)

    def create(self, validated_data):
        request = self.context.get('request')
        data = validated_data.copy()
        data.update({
            'created_by': request.user
        })
        return super(TaskSerializer, self).create(data)

    class Meta:
        model = Task
        fields = '__all__'

