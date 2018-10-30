from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from task.serializers import TaskSerializer
from .models import TaskProject
from .serializers import TaskProjectSerializer


class TaskProjectViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = TaskProjectSerializer
    queryset = TaskProject.objects.all()
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'tasks':
            return TaskSerializer
        return super(TaskProjectViewSet, self).get_serializer_class()

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data.update({
            'created_by': request.user.id
        })
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True)
    def tasks(self, request, slug):
        project = self.get_object()
        queryset = project.task_set.all()
        pk = request.query_params.get('id')
        if pk:
            queryset = queryset.filter(id=pk)
        assignee = request.query_params.get('assignee')
        if assignee:
            queryset = queryset.filter(assignee=assignee)
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data)
