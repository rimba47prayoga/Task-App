from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Task
from .choices import TaskChoices
from .services.create_task import CreateTaskService


class SimpleUserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        if hasattr(obj, 'userprofile'):
            return obj.userprofile.avatar
        return None

    class Meta:
        model = User
        fields = ['id', 'username', 'avatar']


class TaskSerializer(serializers.ModelSerializer):
    assignee = SimpleUserSerializer(allow_null=True)
    created_by = SimpleUserSerializer(allow_null=True, required=False)

    class Meta:
        model = Task
        fields = '__all__'


class CreateTaskSerializer(serializers.Serializer):
    title = serializers.CharField()
    task_type = serializers.ChoiceField(choices=TaskChoices.TASK_TYPE_CHOICES)
    label = serializers.CharField(required=False, allow_blank=True)
    priority = serializers.ChoiceField(choices=TaskChoices.PRIORITY_CHOICES)
    prefix_branch = serializers.CharField()
    branch = serializers.CharField()
    assignee = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )
    progress = serializers.ChoiceField(
        choices=TaskChoices.PROGRESS_CHOICES,
        required=False
    )
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(),
        required=False
    )
    descriptions = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        request = self.context.get('request')
        data = validated_data.copy()
        data.update({
            'created_by': request.user
        })
        service = CreateTaskService(payload=data)
        task = service.execute()
        return task

    class Meta:
        fields = [
            'title', 'task_type', 'label', 'priority', 'prefix_branch',
            'branch', 'assignee', 'progress', 'parent', 'descriptions'
        ]

