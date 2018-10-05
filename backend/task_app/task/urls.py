from rest_framework import routers
from .views import TaskViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'', TaskViewSet)

urlpatterns = router.urls
