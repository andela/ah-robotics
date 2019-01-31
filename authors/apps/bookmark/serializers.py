from rest_framework import serializers
from authors.apps.bookmark.models import BookmarkArticle


class BookmarkSerializer(serializers.ModelSerializer):
    """ Bookmark-article serializer """
    slug = serializers.CharField(source='article.slug')

    class Meta:
        model = BookmarkArticle
        fields = [
            'slug',
            'id'
        ]
