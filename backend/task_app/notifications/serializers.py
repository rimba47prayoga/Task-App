from rest_framework import serializers

from task.models import Task
from task.serializers import SimpleTaskSerializer
from .models import Notifications


class NotificationsSerializer(serializers.ModelSerializer):

    related_data = serializers.SerializerMethodField()

    def get_related_data(self, obj):
        related_data = obj.content_object
        if related_data:
            if isinstance(related_data, Task):
                serializer = SimpleTaskSerializer(instance=related_data)
                return serializer.data
        return None

    class Meta:
        fields = ['id', 'notification_id', 'title', 'message', 'related_data']
        model = Notifications
