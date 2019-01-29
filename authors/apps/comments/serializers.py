from rest_framework import serializers

from .models import Comment
class Commentserializer(serializers.ModelSerializer):
    """
    Create a serializer for the comments model
    """
    author = serializers.SerializerMethodField
    class Meta:
        model = Comment
        fields = ('id','created_at','updated_at','body','author','slug','is_deleted')