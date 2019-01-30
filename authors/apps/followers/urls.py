from django.urls import path

from .views import ListCreateFollow, DeleteFollower

app_name = 'followers'

urlpatterns = [
    path('followers/<username>/',
     DeleteFollower.as_view()
     ),
    path('profiles/<username>/follow',
     ListCreateFollow.as_view(),
      name='followers'
      ),
    path('followers/', ListCreateFollow.as_view(), name='followers')
]
