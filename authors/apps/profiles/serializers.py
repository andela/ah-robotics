from rest_framework import serializers

from .models import UserProfile
from authors.apps.followers.models import Follower

class ProfileSerializer(serializers.ModelSerializer):
    """User Profile object fields"""
    username = serializers.CharField(source='user.username',
                                     read_only=True)
    bio = serializers.CharField()
    image = serializers.ImageField(default=None)
    class Meta:
        model = UserProfile
        fields = ['username', 'bio', 'image',
                'created_at', 'updated_at']
        

class AuthorSerializer(serializers.ModelSerializer):
    """Author object fields"""
    username = serializers.CharField(source='user.username',
                                     read_only=True)
    bio = serializers.CharField()
    image = serializers.ImageField(default=None)

    class Meta:
        model = UserProfile
        fields = ['username', 'bio', 'image']

class FollowSerializer(serializers.ModelSerializer):
    """User Profile object fields"""
    username = serializers.CharField(source='user.username',
                                     read_only=True)
    bio = serializers.CharField()
    image = serializers.ImageField(default=None)
    following_count = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['username', 'bio', 'image',
                'following', 'following_count']

    def get_following_count(self,instance):
        return Follower.objects.filter(user_id=instance.user.id).count()

    def get_following(self,instance):
        request = self.context.get('request')
        user_id = request.user.id
        try:
            follower_exists = Follower.objects.filter(
                user_id=user_id,followed_user_id=instance.user.id).first()
            if follower_exists is not None:
                return True
            return False
        except Follower.DoesNotExist:
            return False