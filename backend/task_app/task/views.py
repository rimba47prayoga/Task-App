from collections import OrderedDict
from datetime import datetime

from django.contrib.auth.models import User
from haystack.query import SearchQuerySet
from haystack.utils.highlighting import Highlighter
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from core.exceptions import TaskAppError
from .models import Task
from .serializers import (
    TaskSerializer, SimpleUserSerializer, CreateTaskSerializer,
    UpdateProgressSerializer
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
        elif self.action == 'update_progress':
            return UpdateProgressSerializer
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
        queryset = self.queryset.values('id', 'title', 'prefix_branch', 'branch')
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

    @action(methods=['put'], detail=True)
    def update_progress(self, request, pk=None):
        instance = self.get_object()
        data = request.data.copy()
        data.update({
            'old_progress': instance.progress
        })
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            instance.progress = serializer.data.get('new_progress')
            instance.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def undo_progress(self, request, pk=None):
        instance = self.get_object()
        if (datetime.now() - instance.modified_date).seconds > 60:
            raise TaskAppError(
                message='Undo time has expire',
                status_code=status.HTTP_400_BAD_REQUEST
            )
        instance.progress -= 1
        instance.save()
        return Response({'progress': instance.progress})


class SearchTaskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Task.objects.none()

    def list(self, request, *args, **kwargs):
        return super(SearchTaskViewSet, self).list(request, *args, **kwargs)

    @action(methods=['get'], detail=False)
    def autocomplete(self, request):
        q = request.query_params.get('q')
        if q:
            search_result = SearchQuerySet().autocomplete(text__icontains=q)
            search_result = map(lambda x: x.title, search_result)
            search_result = {
                'result': list(search_result)
            }
            return Response(search_result)
        return Response([])
