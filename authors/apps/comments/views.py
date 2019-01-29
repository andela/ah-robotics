from django.shortcuts import render
from  rest_framework import viewsets

from .models import Comment
from .serializers import Commentserializer
class CommentsAPIView(viewsets.ModelViewSet):
    """
    Create a view to post, update, delete and get all comments
    """
    queryset  = Comment.objects.all()
    serializer_class = Commentserializer
