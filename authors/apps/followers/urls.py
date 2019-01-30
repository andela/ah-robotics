from django.urls import path

from .views import ListCreateFollow, DeleteFavorite

app_name = 'followers'

urlpatterns = [
    path('follow/', ListCreateFollow.as_view(), name='follow'),
    path('follow/<username>/', DeleteFavorite.as_view())
]
