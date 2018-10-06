from rest_framework import generics
from rest_framework import viewsets

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(generics.ListAPIView,
                  generics.RetrieveAPIView,
                  generics.CreateAPIView,
                  generics.UpdateAPIView,
                  viewsets.GenericViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def list(self, request, *args, **kwargs):
        return super(TaskViewSet, self).list(request, *args, **kwargs)
