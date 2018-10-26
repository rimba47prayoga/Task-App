from rest_framework import routers

from .views import NotificationsViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('list', NotificationsViewSet)

urlpatterns = router.urls
