from django.urls import include, path
from rest_framework import routers

from .views import CommentsAPIView

router = routers.DefaultRouter()
router.register('comments', CommentsAPIView)

urlpatterns = [
    path('', include(router.urls))
]