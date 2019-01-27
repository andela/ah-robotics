from rest_framework import serializers
from .models import UserProfile


class ProfileSerializer(serializers.ModelSerializer):
    # user model fields
    username = serializers.CharField(source='user.username', read_only=True)

    # profile specific model fields

    bio = serializers.CharField()
    image = serializers.ImageField(default=None)

    class Meta:
        model = UserProfile
        fields = ['username', 'bio', 'image', 'created_at', 'updated_at']


class AuthorSerializer(serializers.ModelSerializer):
    # user model fields
    username = serializers.CharField(source='user.username', read_only=True)

    # profile specific model fields
    bio = serializers.CharField()
    image = serializers.ImageField(default=None)

    class Meta:
        model = UserProfile
        fields = ['username', 'bio', 'image']
