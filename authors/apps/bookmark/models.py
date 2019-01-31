from django.db import models
from ..authentication.models import User
from authors.apps.articles.models import Article
from authors.apps.profiles.models import UserProfile
from django.utils.text import slugify


class BookmarkArticle(models.Model):
    """ User Bookmark holder class """
    class Meta:
        unique_together = ('article', 'user')

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user',
        related_name='user'
        )

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        verbose_name='article',
        related_name='article'
        )

    def __str__(self):
        """ Return title of bookmarked article """
        return self.article.slug
