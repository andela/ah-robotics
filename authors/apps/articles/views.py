from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from .models import Article
from .serializers import ArticleSerializers
from .renderers import ArticleJsonRenderer
from authors.apps.core.permissions import IsOwnerOrReadonly


def article_not_found():
    raise ValidationError(
        detail={'error': 'No article found for the slug given'})


def get_article(slug):
    try:
        article = Article.objects.get(slug=slug)
        return article
    except Exception:
        article_not_found()


class ListCreateArticle(ListCreateAPIView):
    queryset = Article.objects.all()
    renderer_classes = (ArticleJsonRenderer,)
    serializer_class = ArticleSerializers
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request):
        article = request.data.get('article', {})
        serializer = self.serializer_class(
            data=article, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetrieveUpdateDeleteArticle(RetrieveUpdateDestroyAPIView):
    """
    Enable Read,Update,Delete operations on a single article instance
    """
    lookup_field = 'slug'
    queryset = Article.objects.all()
    serializer_class = ArticleSerializers
    renderer_classes = (ArticleJsonRenderer,)
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadonly)

    def get(self, request, slug):
        """Get article by using its slug value"""
        article = get_article(slug)
        if not article:
            article_not_found()

        return super().get(request, slug)

    def update(self, request, slug):
        """
        Update an article
        """
        try:
            article = Article.objects.get(slug=slug)
        except Exception:
            article_not_found()
            return Response(status=status.HTTP_404_NOT_FOUND)

        article_data = request.data.get('article', {})
        serializer = self.serializer_class(
            article, data=article_data, partial=True)

        if serializer.is_valid():
            self.check_object_permissions(request, article)
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        """
        Delete an article
        """
        if not get_article(slug):
            article_not_found()

        super().delete(self, request, slug)
        return Response({"message": "article deleted successfully"})
