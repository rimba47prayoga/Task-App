from rest_framework import mixins, status, viewsets

from .models import Notifications
from .serializers import NotificationsSerializer


class NotificationsViewSet(mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    serializer_class = NotificationsSerializer
    queryset = Notifications.objects.all()

    def get_queryset(self):
        request = self.request
        queryset = self.queryset.filter(user=request.user)
        return queryset
