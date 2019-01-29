from rest_framework import status
from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from authors.apps.articles.models import Article
from authors.apps.core.permissions import IsOwnerOrReadonly

from .models import Favorite
from .serializers import FavoriteInputSerializer, FavoriteInfoSerializer
from .renderers import FavoriteJsonRenderer


class ListCreateFavorite(ListCreateAPIView):
    """
    Provide view for adding an article to favorites
    and a view for displaying a list of favorites articles
    """
    queryset = Favorite.objects.all()
    serializer_class = FavoriteInfoSerializer
    renderer_classes = (FavoriteJsonRenderer,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request):
        """
        Add an article to the user's favorites
        """
        slug = request.data.get('article_slug')
        article_exists = Article.objects.filter(slug=slug).exists()
        if not article_exists:
            return Response({'error': 'article with given slug not found'},
                            status.HTTP_404_NOT_FOUND)
        article = Article.objects.get(slug=slug)
        favorite_existence = Favorite.is_article_in_user_favorites(
            article_id=article.id,
            user_id=self.request.user.id)
        if favorite_existence:
            return Response({'error': 'article already exists in favorites'},
                            status.HTTP_400_BAD_REQUEST)

        data = {"article": article.id, "user": self.request.user.id}
        serializer = FavoriteInputSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message': 'article added to favorites'},
                        status.HTTP_201_CREATED)

    def get(self, request):
        queryset = Favorite.objects.filter(user=self.request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteFavorite(DestroyAPIView):
    """
    Delete view to allow user to remove article from favorites
    """
    queryset = Favorite.objects.all()
    serializer_class = FavoriteInfoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadonly)

    def delete(self, request, slug):
        """
        Delete article from user favorites
        """
        article_exists = Article.objects.filter(slug=slug).exists()
        if not article_exists:
            return Response({'error': 'article with given slug not found'},
                            status.HTTP_404_NOT_FOUND)
        article = Article.objects.get(slug=slug)
        favorite_existence = Favorite.is_article_in_user_favorites(
            article_id=article.id,
            user_id=request.user.id)

        if favorite_existence:
            instance = Favorite.objects.filter(
                user=self.request.user.id, article=article.id)

            instance.delete()
            return Response({'message': 'article removed from favorites'},
                            status.HTTP_200_OK)
        return Response({'message': 'article not in favorites'},
                        status.HTTP_404_NOT_FOUND)
