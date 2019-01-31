from rest_framework import serializers

from .models import Follower


class FollowerSerializer(serializers.ModelSerializer):
    """Serializer to follow another user"""

    class Meta:
        model = Follower
        fields = ['user', 'followed_user']


class FollowerInfoSerializer(serializers.BaseSerializer):
    """
    Follower serializer to display the username of the follower
    """
    def to_representation(self, obj):
        return {
            'username': obj.followed_user.username,
        }
