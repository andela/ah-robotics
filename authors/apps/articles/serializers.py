import datetime
import math
import re

from django.db.models import Avg
from rest_framework import serializers
from taggit_serializer.serializers import (
    TagListSerializerField, TaggitSerializer)

from authors.apps.favorites.models import Favorite
from authors.apps.profiles.models import UserProfile
from authors.apps.profiles.serializers import AuthorSerializer
from .models import Article, Reaction
from ..rating.models import Rating


class ArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    title = serializers.CharField(
        required=True,
        max_length=500,
        error_messages={
            'required': 'article title cannot be empty',
            'max_length': 'article title cannot exceed 500 characters'
        }
    )
    description = serializers.CharField(
        required=False,
        max_length=1000,
        error_messages={
            'max_length': 'description cannot exceed 1000 characters'
        }
    )
    body = serializers.CharField(
        required=True,
        error_messages={
            'required': 'article body cannot be empty'
        }
    )
    image = serializers.ImageField(default=None)
    author = serializers.SerializerMethodField(read_only=True)
    tagList = TagListSerializerField()
    rating = serializers.SerializerMethodField(read_only=True)
    favorited = serializers.SerializerMethodField(read_only=True)
    favorite_count = serializers.SerializerMethodField(read_only=True)
    read_time = serializers.SerializerMethodField()
    like_status = serializers.SerializerMethodField()
    dislike_status = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()

    def get_author(self, obj):
        """Get the profile of the author of the article"""
        serializer = AuthorSerializer(
            instance=UserProfile.objects.get(user=obj.author))
        return serializer.data

    def get_rating(self, obj):
        """Return an article rating"""
        average_rating = Rating.objects.filter(
            article__slug=obj.slug).aggregate(Avg('user_rating'))
        response = {"average_rating": average_rating['user_rating__avg']}
        if average_rating['user_rating__avg'] is None:
            average_rating['user_rating__avg'] = 0
            return response

        return response

    def get_favorited(self, instance):
        request = self.context.get("request")
        return Favorite.is_article_in_user_favorites(
            article_id=instance.id, user_id=request.user.id)

    def get_favorite_count(self, instance):
        return Favorite.get_count_for_article(article_id=instance.id)

    def get_read_time(self, instance):
        """ Get the body of the article instance """
        content = instance.body
        """ Get words from the body content """
        words = re.findall(r'\w+', content)
        """ Get word count """
        word_count = len(words)

        """
        Get read time in minutes
        Assumption is made that an individual will read  an average of
        200 words per minute
        """
        time = math.ceil(word_count/200)
        """ Return time value in date format """
        read_time = str(datetime.timedelta(minutes=time))
        return read_time

    def get_likes(self, instance):
        return instance.reaction.likes().count()

    def get_dislikes(self, instance):
       return instance.reaction.dislikes().count()

    def get_like_status(self,instance):
        request = self.context.get("request")
        if instance.reaction.filter(user_id=request.user.id,reaction=1):
           return True
        return False
        
    def get_dislike_status(self,instance):
        request = self.context.get("request")
        if instance.reaction.filter(user_id=request.user.id,reaction=-1):
           return True
        return False


    class Meta:
        model = Article
        fields = ('slug', 'title', 'description',
                  'body', 'image', 'created_at', 'updated_at',
                  'favorited', 'favorite_count', 'author', 'tagList',
                  'rating', 'read_time', 'likes', 'dislikes','like_status','dislike_status')


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
