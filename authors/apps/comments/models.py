from django.db import models

from authors.apps.authentication.models import User
from authors.apps.articles.models import Article
from authors.apps.core.models import TimestampMixin


class Comment(TimestampMixin,models.Model):
    """
    Create a comments model
    """
    body = models.TextField(blank=False, null=False)
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
    slug = models.ForeignKey(
        Article, 
        on_delete=models.CASCADE
    )
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.body

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
