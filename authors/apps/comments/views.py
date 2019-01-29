from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Comment
from .serializers import Commentserializer
from authors.apps.articles.models import Article


class CommentsAPIView(APIView):
    """
    Create a view to post, update, delete and get all comments
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = Commentserializer

    def get(self, request, **kwargs):
        slug = self.kwargs['slug']
        article = Article.objects.filter(slug=slug).first()

        if not article:
            return Response(
                {
                    "comment": {
                        "error": "Article not found"
                    }
                },
                status=status.HTTP_404_NOT_FOUND
            )

        queryset = Comment.objects.filter(article=article.id)
        if not queryset:
            return Response(
                {
                    "comment": {
                        "error": "You dont have any comments yet"
                    }
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(data=queryset, many=True)
        serializer.is_valid()
        return Response({
            "comment": serializer.data,
            "commentsCount": queryset.count()
        },
            status=status.HTTP_200_OK
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, **kwargs):
        slug = self.kwargs['slug']
        article = Article.objects.get(slug=slug)
        comment = request.data.get('comment', {})
        serializer = self.serializer_class(data=comment, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user, article=article)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OneCommentAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, update, and delete a given comment
    """

    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = Commentserializer

    def get(self, request, id, *args, **kwargs):
        """
        Get a comment by id
        """
        slug = self.kwargs['slug']
        article = Article.objects.filter(slug=slug).first()

        if not article:
            return Response(
                {
                    "comment": {
                        "error": "Article not found"
                    }
                },
                status=status.HTTP_404_NOT_FOUND
            )
        queryset = Comment.objects.filter(id=id, article=article.id)
        if not queryset:
            return Response(
                {
                    "comment": {
                        "error": "Comment not found"
                    }
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(queryset, many=True)
        return Response({
            "comment": serializer.data[0]
        },
            status=status.HTTP_200_OK
        )

    def destroy(self, request, id, *args, **kwargs):
        """
        Delete a comment by id
        """
        slug = self.kwargs['slug']
        article = Article.objects.filter(slug=slug).first()

        if not article:
            return Response(
                {
                    "comment": {
                        "message": "Article not found"
                    }
                },
                status=status.HTTP_404_NOT_FOUND
            )
        queryset = Comment.objects.filter(id=id, article=article.id)
        if not queryset:
            return Response(
                {
                    "comment": {
                        "message": "Comment not found"
                    }
                },
                status=status.HTTP_404_NOT_FOUND
            )
        queryset[0].delete()
        return Response(
            {
                "comment": {
                    "message": "Comment deleted successfully"
                }
            },
            status=status.HTTP_200_OK
        )

    def update(self, request, id, *args, **kwargs):
        """
        Delete a comment by id
        """
        slug = self.kwargs['slug']
        article = Article.objects.filter(slug=slug).first()

        if not article:
            return Response(
                {
                    "comment": {
                        "message": "Article not found"
                    }
                },
                status=status.HTTP_404_NOT_FOUND
            )
        comment = Comment.objects.filter(id=id, article=article.id).first()
        if not comment:
            return Response(
                {
                    "comment": {
                        "message": "Comment not found"
                    }
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if request.user.pk != comment.author.id:
            return Response(
                {
                    "comment": {
                        "message": "You are not authorized to comment"
                    }
                },
                status=status.HTTP_404_NOT_FOUND
            )

        comment_data = request.data.get('comment', {})
        comment.body = comment_data['body']
        comment.save(update_fields=['body'])
        return Response(
            {
                "comment": {
                    "message": "Comment Updated successfully"
                }
            },
            status=status.HTTP_200_OK
        )
