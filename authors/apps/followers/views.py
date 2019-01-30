from rest_framework.generics import (
    ListCreateAPIView, DestroyAPIView)
from authors.apps.authentication.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from authors.apps.core.permissions import IsOwnerOrReadonly

from .models import Follower
from .serializers import FollowerSerializer, FollowerInfoSerializer
from .renderers import FollowerJsonRenderer


class ListCreateFollow(ListCreateAPIView):
    queryset = Follower.objects.all()
    serializer_class = FollowerInfoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (FollowerJsonRenderer,)

    def post(self, request):
        """
        Add an article to the user's favorites
        """
        username = request.data.get('username')
        user_exists = User.objects.filter(username=username).exists()
        if not user_exists:
            return Response(
                {'error': 'user with that name was not found'},
                            status.HTTP_404_NOT_FOUND)
        user_to_follow = User.objects.get(username=username)
        already_followed = Follower.is_user_already_followed(
            user_to_follow_id=user_to_follow.id,
            user_id=self.request.user.id
            )
        if already_followed:
            return Response({'error': 'user already followed'},
                            status.HTTP_400_BAD_REQUEST)

        data = {
            "user_to_follow": user_to_follow.id,
             "user": self.request.user.id}
        serializer = FollowerSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message': 'user followed successfully'},
                        status.HTTP_201_CREATED)

    def get(self, request):
        queryset = Follower.objects.filter(user=self.request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteFavorite(DestroyAPIView):
    """
    Delete view to allow user to remove article from favorites
    """
    queryset = Follower.objects.all()
    serializer_class = FollowerInfoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadonly)

    def delete(self, request, username):
        """
        Delete article from user favorites
        """
        user_to_follow_exists = User.objects.filter(username=username).exists()
        if not user_to_follow_exists:
            return Response({'error': 'user not found'},
                            status.HTTP_404_NOT_FOUND)
        user_to_follow = User.objects.get(username=username)
        user_exists = Follower.is_user_already_followed(
            user_to_follow_id=user_to_follow.id,
            user_id=request.user.id
            )
        if user_exists:
            instance = Follower.objects.filter(
                user=self.request.user.id, user_to_follow=user_to_follow.id
                )
            instance.delete()
            return Response({'message': 'user unfollowed'},
                            status.HTTP_200_OK)
        return Response({'message': 'user not in followers'},
                        status.HTTP_404_NOT_FOUND)