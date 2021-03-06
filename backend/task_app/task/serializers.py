from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers

from notifications.choices import ASSIGNEE_TASK, UN_ASSIGNEE_TASK
from notifications.tasks import NotificationTask
from project.models import TaskProject
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
    branch = serializers.SerializerMethodField()
    deadline = serializers.DateField(format='%d/%m/%Y')
    created_by = SimpleUserSerializer(allow_null=True, required=False)

    def get_branch(self, obj):
        return f'{obj.project.board_name}-{obj.branch}'

    class Meta:
        model = Task
        exclude = ['is_deleted', 'deleted_time']


class CreateTaskSerializer(serializers.Serializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=TaskProject.objects.all()
    )
    title = serializers.CharField()
    task_type = serializers.ChoiceField(choices=TaskChoices.TASK_TYPE_CHOICES)
    label = serializers.CharField(required=False, allow_blank=True)
    priority = serializers.ChoiceField(choices=TaskChoices.PRIORITY_CHOICES)
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
    deadline = serializers.DateField()
    descriptions = serializers.CharField(required=False, allow_blank=True)

    @transaction.atomic
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
            'title', 'task_type', 'label', 'priority',
            'assignee', 'progress', 'parent', 'deadline',
            'descriptions'
        ]


class UpdateTaskSerializer(serializers.ModelSerializer):
    assignee = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )

    def update(self, instance, validated_data):
        user = self.context.get('request').user  # current user
        assignee = validated_data.get('assignee')  # recipient
        if assignee:
            # assignee to other user
            if assignee != instance.assignee:
                if assignee != user:
                    payload = {
                        'title': f'{user.username} assigned an task to you.',
                        'recipient': assignee.id,  # celery can't receive class object
                        'subject': ASSIGNEE_TASK,
                        'related_data': instance.id
                    }
                else:
                    payload = {
                        'title': f'{user.username} unassigned an task from you.',
                        'recipient': instance.assignee.id,
                        'subject': UN_ASSIGNEE_TASK,
                        'related_data': instance.id
                    }
                NotificationTask.task_push_notification.delay(payload)
        return super(UpdateTaskSerializer, self).update(instance, validated_data)

    class Meta:
        model = Task
        exclude = ['is_deleted', 'deleted_time']


class UpdateProgressSerializer(serializers.Serializer):
    old_progress = serializers.ChoiceField(choices=TaskChoices.PROGRESS_CHOICES)
    new_progress = serializers.ChoiceField(choices=TaskChoices.PROGRESS_CHOICES)

    def validate(self, attrs):
        old_progress = attrs.get('old_progress')
        new_progress = attrs.get('new_progress')
        if (new_progress - old_progress) > 1:
            progress_choices = dict(TaskChoices.PROGRESS_CHOICES)
            message = ('Please change task progress to {new_progress} before {'
                       'next_progress}').format(
                new_progress=progress_choices.get(new_progress).lower(),
                next_progress=progress_choices.get(old_progress + 1).lower()
            )
            raise serializers.ValidationError({
                'message': message,
                'error_field': 'new_progress'
            })
        if new_progress < old_progress:
            raise serializers.ValidationError({
                'message': 'Cannot change task progress to step back',
                'error_field': 'new_progress'
            })
        return super(UpdateProgressSerializer, self).validate(attrs)

    class Meta:
        fields = ['old_progress', 'new_progress']


class SimpleTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'title', 'task_type', 'priority', 'branch_name']
