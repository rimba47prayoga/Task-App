from collections import OrderedDict

from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Task
from .serializers import (
    TaskSerializer, SimpleUserSerializer, CreateTaskSerializer
)


class TaskViewSet(generics.ListAPIView,
                  generics.RetrieveAPIView,
                  generics.CreateAPIView,
                  generics.UpdateAPIView,
                  viewsets.GenericViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.action == 'assignee_task':
            return SimpleUserSerializer
        elif self.action == 'create':
            return CreateTaskSerializer
        return super(TaskViewSet, self).get_serializer_class()

    def list(self, request, *args, **kwargs):
        import time
        time.sleep(1)
        return super(TaskViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def parent_task(self, request):
        queryset = self.queryset.values('id', 'title', 'branch')
        import time
        time.sleep(1)
        return Response(queryset)

    @action(methods=['get'], detail=False)
    def assignee_task(self, request):
        queryset = User.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def generate_branch(self, request):
        result = OrderedDict([
            ('branch', Task.generate_branch())
        ])
        return Response(result)
