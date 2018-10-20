from django.urls import include, path
from rest_framework import routers
from .views import TaskViewSet, SearchTaskViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'list', TaskViewSet)
router.register('search', SearchTaskViewSet)

urlpatterns = [
    path('full_search', include('haystack.urls'))
]

urlpatterns += router.urls
