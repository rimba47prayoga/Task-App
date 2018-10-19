from rest_framework import routers

from .views import TaskProjectViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'', TaskProjectViewSet)

urlpatterns = router.urls
