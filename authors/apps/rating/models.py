from django.db import models

from ..articles.models import Article
from ..authentication.models import User

class Rating(models.Model):
    """ Rating model Schema"""
    user = models.ForeignKey(
        User,
        related_name="rater",
        on_delete=models.CASCADE
    )
    article = models.ForeignKey(
        Article,
        related_name="rated_article",
        on_delete=models.CASCADE
    )
    user_rating = models.FloatField(null=False)

    def __str__(self):
        return self.user_rating
