from django.urls import path, include

urlpatterns = [
    path('task/', include('task.urls')),
    path('auth/', include('task_user.urls'))
]
