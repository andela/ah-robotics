from django.db import models
from authors.settings import AUTH_USER_MODEL
from authors.apps.authentication.models import User

# Create your models here.
class Follower(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='follower')
    user_to_follow = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followee')


    def get_follower_count(self, user_id):
        follower_count = Follower.objects.filter(
            user=user_id).count()
        return follower_count

    def get_following_count(self, user_id):
        following_count = Follower.objects.filter(
            user_to_follow=user_id).count()
        return following_count

    @staticmethod
    def is_user_already_followed(user_to_follow_id, user_id):
        """
        Check if user is already followed
        """
        result = Follower.objects.filter(user_to_follow=user_to_follow_id,
                                         user=user_id).exists()
        return result

            