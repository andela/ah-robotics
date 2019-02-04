from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from cloudinary.models import CloudinaryField

from authors.settings import AUTH_USER_MODEL
from authors.apps.core.models import TimestampMixin
from authors.apps.authentication.models import User


class UserProfile(TimestampMixin, models.Model):
    """
    This model creates user profile once a user account is created.
    The user profile comprises of bio and the image field
    """
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='profile')
    bio = models.TextField(default="Update your profile")
    image = CloudinaryField(
        "image",
        default="https://res.cloudinary.com/dy2faavdk/image/upload/v1548264034/qvxtpdmi03kksg9rxgfj.png")

    @property
    def username(self):
        return self.user.username

    def __str__(self):
        return self.user.username

    """
    This method creates user profile everytime a user is created
    The user profile is linked to the user account
    """
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    """
    This method saves user profile on user save event
    """
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
