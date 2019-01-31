from django.db import models

from authors.settings import AUTH_USER_MODEL
from authors.apps.authentication.models import User


class Follower(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='follower')
    followed_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followee')

    @staticmethod
    def is_user_already_followed(followed_user_id, user_id):
        """
        Check if user is already followed
        """
        result = Follower.objects.filter(followed_user=followed_user_id,
                                         user=user_id).exists()
        return result
