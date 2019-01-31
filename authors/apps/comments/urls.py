from django.urls import path

from .views import CommentsAPIView, OneCommentAPIView

app_name = 'comments'
urlpatterns = [
    path('articles/<slug:slug>/comments/',
         CommentsAPIView.as_view(),
         name='comments'
         ),
    path('articles/<slug:slug>/comments/<int:id>/',
         OneCommentAPIView.as_view(),
         name='specific_comment'
         ),
]
