from calendar import timegm
from datetime import datetime

from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import jwt_response_payload_handler

from core.exceptions import TaskAppError, TaskAppErrorCode
from .models import UserProfile

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        exclude = ['id']


class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    def get_profile(self, obj):
        if hasattr(obj, 'userprofile'):
            return UserProfileSerializer(instance=obj.userprofile).data
        return None

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'profile',
            'last_login'
        ]


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        try:
            user = User.objects.get(username=attrs.get('username'))
        except User.DoesNotExist:
            raise TaskAppError(
                message="You're not registered, please register first",
                status_code=status.HTTP_400_BAD_REQUEST,
                error_code=TaskAppErrorCode.USER_NOT_REGISTERED,
            )
        else:
            if not user.check_password(attrs.get('password')):
                msg = "You can't login, your password is incorrect"
                raise TaskAppError(
                    message=msg,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    error_code=TaskAppErrorCode.INCORRECT_PASSWORD,
                )
        self.user = user
        return attrs

    def login(self):
        payload = jwt_payload_handler(self.user)
        if api_settings.JWT_ALLOW_REFRESH:
            payload['orig_iat'] = timegm(datetime.utcnow().utctimetuple())

        request = self.context.get('request')
        token = jwt_encode_handler(payload)

        response = jwt_response_payload_handler(token, self.user, request)
        response['user'] = UserSerializer(instance=self.user).data
        return response
