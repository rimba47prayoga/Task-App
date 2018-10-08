from django.utils import timezone
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class TaskAppAuthentication(JSONWebTokenAuthentication):

    def authenticate(self, request):
        try:
            user, jwt_value = super(TaskAppAuthentication, self).authenticate(request)
            # Renew last login.
            user.last_login = timezone.now()
            user.save()
            return user, jwt_value
        except TypeError:
            pass
