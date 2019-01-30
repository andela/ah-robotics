from django.contrib.contenttypes.models import ContentType

from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from authors.apps.core.permissions import IsOwnerOrReadonly

from .models import Article, Reaction
from .serializers import ArticleSerializers, ReactionSerializer
from .renderers import ArticleJsonRenderer


def article_not_found():
    raise ValidationError(
        detail={'error': 'No article found for the slug given'})


def get_article(slug):
    """
    Returns article with the given slug if exists
    or returns an exception if no article with slug exists
    """
    try:
        article = Article.objects.get(slug=slug)
        return article
    except Exception:
        article_not_found()
        return Response(status=status.HTTP_404_NOT_FOUND)


class ListCreateArticle(ListCreateAPIView):
    queryset = Article.objects.all()
    renderer_classes = (ArticleJsonRenderer,)
    serializer_class = ArticleSerializers
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request):
        """
        Create an article
        """
        article = request.data.get('article', {})
        serializer = self.serializer_class(
            data=article, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        queryset = Article.objects.all()
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        """
        Get article by using its slug value
        """
        article = get_article(slug)
        if not article:
            article_not_found()

        return super().get(request, slug)

    def update(self, request, slug):
        """
        Update an article
        """
        article = get_article(slug)

        article_data = request.data.get('article', {})
        serializer = self.serializer_class(
            article, data=article_data, partial=True, context={'request': request})

        if serializer.is_valid():
            self.check_object_permissions(request, article)
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, slug):
        """
        Update selective details of an article
        """
        article = get_article(slug)

        article_data = request.data
        serializer = self.serializer_class(
            instance=article, data=article_data, partial=True)

        if serializer.is_valid():
            self.check_object_permissions(request, article)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        """
        Delete an article
        """
        if not get_article(slug):
            article_not_found()

        super().delete(self, request, slug)
        return Response({"message": "article deleted successfully"})


class ReactionView(CreateAPIView):
    """
    This class returns reaction objects
    The reaction object contains article likes and dislikes
    """
    model = None
    reaction_type = None
    serializer_class = ReactionSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, slug):
        article = get_article(slug)
        try:
            """
            fetch existing user likes and dislikes on an article
            """
            likedislike = Reaction.objects.get(
                content_type=ContentType.objects.get_for_model(article),
                object_id=article.id,
                user=request.user
            )
            """
            toggle the article reaction
            """
            if likedislike.reaction is not self.reaction_type:
                likedislike.reaction = self.reaction_type
                likedislike.save(update_fields=['reaction'])
                result = True
            else:
                likedislike.delete()
                result = False
        except Reaction.DoesNotExist:
            # create new reaction
            article.reaction.create(user=request.user,
                                    reaction=self.reaction_type)
            result = True
        return Response({
            "status": result,
            "likes": article.reaction.likes().count(),
            "dislikes": article.reaction.dislikes().count(),
            "total": article.reaction.sum_rating()
        },
            content_type="application/json",
            status=status.HTTP_201_CREATED
        )
