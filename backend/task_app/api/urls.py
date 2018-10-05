from django.urls import path, include

urlpatterns = [
    path('task/', include('task.urls'))
]
