from rest_framework import serializers

from authors.apps.profiles.serializers import ProfileSerializer
from authors.apps.profiles.models import UserProfile
from .models import Comment


class Commentserializer(serializers.ModelSerializer):
    """
    Create a serializer for the comments model
    """
    author = serializers.SerializerMethodField()
    article = serializers.SerializerMethodField()
    body = serializers.CharField(
        required=True,
        error_messages={
            'required': 'comment body cannot be empty',
        }
    )

    class Meta:
        model = Comment
        fields = ('id', 'created_at', 'updated_at', 'body',
                  'author', 'article')

        read_only_fields = ('id', 'author',
                            'created_at', 'updated_at', 'article')

    def get_author(self, obj):
        serializer = ProfileSerializer(
            instance=UserProfile.objects.get(user=obj.author))
        return serializer.data

    def get_article(self, obj):
        return obj.article.id
