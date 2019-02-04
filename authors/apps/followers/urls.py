from django.urls import path

from .views import ListCreateFollow, DeleteFollower, FollowersView, RetrieveFollowing

app_name = 'followers'

urlpatterns = [
    path('profiles/<username>/unfollow', DeleteFollower.as_view(), name='delete_url'),
    path('profiles/<username>/follow', ListCreateFollow.as_view(),
         name='follow_url'),
    path('profiles/<username>/following/', RetrieveFollowing.as_view(), name='following_url'),
    path('profiles/<username>/followers/', FollowersView.as_view(), name='followers_url')
]
