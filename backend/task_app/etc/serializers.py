from rest_framework import serializers

from .models import UserProfile


class SimpleUserProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = UserProfile
        fields = ['username', 'avatar']
