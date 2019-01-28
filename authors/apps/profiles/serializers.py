from rest_framework import serializers

from .models import UserProfile


class ProfileSerializer(serializers.ModelSerializer):
    """User Profile object fields"""
    username = serializers.CharField(source='user.username',
                                     read_only=True)
    bio = serializers.CharField()
    image = serializers.ImageField(default=None)

    class Meta:
        model = UserProfile
        fields = ['username', 'bio', 'image', 'created_at', 'updated_at']


class AuthorSerializer(serializers.ModelSerializer):
    """Author object fields"""
    username = serializers.CharField(source='user.username',
                                     read_only=True)
    bio = serializers.CharField()
    image = serializers.ImageField(default=None)

    class Meta:
        model = UserProfile
        fields = ['username', 'bio', 'image']
