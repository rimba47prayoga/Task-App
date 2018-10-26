from rest_framework import serializers

from .models import Notifications


class NotificationsSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['id', 'title', 'message']
        model = Notifications
