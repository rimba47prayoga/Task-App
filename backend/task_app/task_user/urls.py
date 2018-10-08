from django.urls import path

from .views import UserLoginViewSet


urlpatterns = [
    path('login', UserLoginViewSet.as_view())
]
