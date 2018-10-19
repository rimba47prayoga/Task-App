from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from .models import TaskProject
from .serializers import TaskProjectSerializer


class TaskProjectViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = TaskProjectSerializer
    queryset = TaskProject.objects.all()

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
