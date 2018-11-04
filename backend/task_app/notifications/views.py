from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

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

    @action(methods=['get'], detail=False)
    def unread_count(self, request):
        count = self.get_queryset().filter(is_read=False).count()
        return Response(
            {
                "count": count
            }
        )
