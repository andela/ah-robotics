from django.urls import path
from .views import BookmarkAPIView, BookmarkListAPIView

app_name = "bookmark"

urlpatterns = [
    path('articles/<slug>/bookmark/',
         BookmarkAPIView.as_view(), name='bookmark-article'),
    path('articles/bookmark/all/',
         BookmarkListAPIView.as_view(), name='get-bookmark'),
]
