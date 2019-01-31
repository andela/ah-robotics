from django.urls import path

from .views import ListCreateFollow, DeleteFollower

app_name = 'followers'

urlpatterns = [
    path('follow/<username>/', DeleteFollower.as_view(), name='delete_url'),
    path('profiles/<username>/follow', ListCreateFollow.as_view(),
         name='follow_url'),
    path('following/', ListCreateFollow.as_view(), name='following_url')
]
