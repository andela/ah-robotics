from django.db import models
from ..authentication.models import User
from ..articles.models import Article


class Notification(models.Model):
    """ """
    article = models.ForeignKey(
        Article,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    user_notification = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    notified = models.ManyToManyField(
        User, related_name='notified', blank=True
    )

    read = models.ManyToManyField(
        User, related_name='read', blank=True
    )

    notification_type = models.TextField(default="article")

    def __str__(self):
        return self.user_notification
