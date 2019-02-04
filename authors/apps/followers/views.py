from rest_framework.generics import (ListCreateAPIView,
                                     DestroyAPIView,
                                     RetrieveUpdateAPIView)
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from .serializers import FollowerSerializer, FollowerInfoSerializer, FollowerListSerializer
from .renderers import FollowerJsonRenderer, FollowerListJsonRenderer

from .models import Follower
from authors.apps.core.permissions import IsOwnerOrReadonly
from authors.apps.authentication.models import User

def user_not_found():
    raise ValidationError(
        {'error': 'No user found for the username given'})


class ListCreateFollow(ListCreateAPIView):
    queryset = Follower.objects.all()
    serializer_class = FollowerInfoSerializer
    permission_classes = (IsAuthenticated,)
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


class RetrieveFollowing(ListCreateAPIView):
    """
    Enable Read operation on a single user instance
    """
    #lookup_field = 'username'
    queryset = Follower.objects.all()
    serializer_class = FollowerInfoSerializer
    renderer_classes = (FollowerJsonRenderer,)
    permission_classes = (IsAuthenticated,)

    def get(self, request,**kwargs):
        username= kwargs.get('username')
        """
        Get userlist by using the username value
        """
        user = User.objects.filter(username=username).first()
        if not user:
            user_not_found()
        following_list = Follower.objects.filter(user=user)
        serializer = self.serializer_class(following_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
class FollowersView(ListCreateAPIView):
    queryset = Follower.objects.all()
    serializer_class = FollowerListSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (FollowerListJsonRenderer,)

    def get(self, request, **kwargs):
        username = kwargs.get('username')
        user = User.objects.filter(username=username).first()
        if not user:
            user_not_found()
        queryset = Follower.objects.filter(followed_user=user)
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
