from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Rating
from django.db.models import Avg


class RatingSerializer(serializers.ModelSerializer):
    """ Serializers for the Rating Model"""
    maximum_rating = 5
    minimum_rating = 1
    user_rating = serializers.IntegerField(
        required=True,
        validators=[
            MinValueValidator(minimum_rating, message="The minimum allowed rating is 1"),
            MaxValueValidator(maximum_rating, message="The maximum allowed rating is 5")
        ],
        error_messages={
            'required': 'Please provide a valid rating'
        }
    )
    article = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    def get_average_rating(self, obj):
        """Returns an average rating for an article"""
        average_rating = Rating.objects.filter(
            article=obj.article.id).aggregate(Avg('user_rating'))
        return average_rating['user_rating__avg']

    def get_article(self, obj):
        """Returns article based on slug"""
        return obj.article.slug

    class Meta:
        model = Rating
        fields = ('article', 'average_rating', 'user_rating')
