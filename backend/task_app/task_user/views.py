from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_jwt.views import ObtainJSONWebToken

from .serializers import UserLoginSerializer


class UserLoginViewSet(GenericAPIView, ObtainJSONWebToken):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            response = serializer.login()
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
