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

    def post(self, request, username):
        """
        Follow a user
        """
        user_exists = User.objects.filter(username=username).exists()
        if not user_exists:
            return Response(
                {'error': 'user with that name was not found'},
                            status.HTTP_404_NOT_FOUND)
        followed_user = User.objects.get(username=username)
        already_followed = Follower.is_user_already_followed(
            followed_user_id=followed_user.id,
            user_id=self.request.user.id
            )
        if already_followed:
            return Response({'error': 'user already followed'},
                            status.HTTP_400_BAD_REQUEST)
        if followed_user.id == self.request.user.id:
            return Response({'error': "you cannot follow yourself."},
                            status.HTTP_400_BAD_REQUEST)
        data = {
            "followed_user": followed_user.id,
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


class DeleteFollower(DestroyAPIView):
    """
    Delete view to allow user to unfollow another user
    """
    queryset = Follower.objects.all()
    serializer_class = FollowerInfoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadonly)

    def delete(self, request, username):
        """
        Remove a user from followers
        """
        followed_user_exists = User.objects.filter(username=username).exists()
        if not followed_user_exists:
            return Response({'error': 'user not found'},
                            status.HTTP_404_NOT_FOUND)
        followed_user = User.objects.get(username=username)
        user_exists = Follower.is_user_already_followed(
            followed_user_id=followed_user.id,
            user_id=request.user.id
            )
        if user_exists:
            instance = Follower.objects.filter(
                user=self.request.user.id, followed_user=followed_user.id
                )
            instance.delete()
            return Response({'message': 'user unfollowed'},
                            status.HTTP_200_OK)
        return Response({'message': 'user not in followers'},
                        status.HTTP_404_NOT_FOUND)