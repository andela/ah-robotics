from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    GenericAPIView
)
from .models import Article, Rating
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated
)
from rest_framework.exceptions import NotFound, ValidationError
from .serializers import RatingSerializer
from rest_framework.response import Response
from rest_framework import serializers, status
from django.db.models import Avg


class RatingAPIView(GenericAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_article(self, slug):
        """Returns specific article based on slug"""
        article = Article.objects.all().filter(slug=slug).first()
        return article

    def get_rating(self, user, article):
        """Returns user article rating"""
        try:
            return Rating.objects.get(user=user, article=article)
        except Rating.DoesNotExist:
            raise NotFound(
                detail={'rating': 'You have not yet rated this article'})

    def post(self, request, slug):
        """POST Request to rate an article"""
        rating = request.data
        article = self.get_article(slug)

        if not article:
            raise ValidationError(
                detail={'message': 'Article not found'}
            )
        if request.user.id == article.author.id:
            return Response({
                "message": "You cannot rate your own article"
            }, status=status.HTTP_403_FORBIDDEN)
        try:
            current_article_rating = Rating.objects.get(
                user=request.user.id,
                article=article.id
            )
            serializer = self.serializer_class(
                current_article_rating, data=rating)
        except Rating.DoesNotExist:
            serializer = self.serializer_class(data=rating)

        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, article=article)
        return Response({
            'message': 'Rating submitted sucessfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def get(self, request, slug):
        """Return an article ratings"""
        article = self.get_article(slug)
        rating = None

        if not article:
            raise ValidationError(
                detail={'message': 'Article not found'}
            )
        if request.user.is_authenticated:
            rating = Rating.objects.get(user=request.user, article=article)

        if rating is None:
            avg = Rating.objects.filter(
                article=article).aggregate(Avg('user_rating'))

            average_rating = avg['user_rating__avg']
            if avg['user_rating__avg'] is None:
                average_rating = 0

            if request.user.is_authenticated is False:
                return Response({
                    'article': article.slug,
                    'average_rating': average_rating,
                    'user_rating': 'Kindly login to rate an article'
                }, status=status.HTTP_200_OK)
        # import pdb; pdb.set_trace()
        serializer = self.serializer_class(rating)
        return Response({
            'message': 'article rating',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def delete(self, request, slug):
        """Delete a Rating from an article"""
        article = self.get_article(slug)
        if not article:
            raise ValidationError(
                detail={'message': 'Article not found'})
        elif article.author != request.user:
            rating = self.get_rating(user=request.user, article=article)
            rating.delete()
            return Response(
                {'message': 'Rating deleted successfully'},
                status=status.HTTP_200_OK)
        else:
            raise ValidationError(
                detail='You cannot delete this rating')
