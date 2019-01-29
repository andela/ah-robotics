from django.db import models

from authors.apps.authentication.models import User
from authors.apps.articles.models import Article


class Favorite(models.Model):
    """
    Model representation of a favorite instance
    """
    article = models.ForeignKey(Article, related_name='articles',
                                on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             related_name='users',
                             on_delete=models.CASCADE)

    @staticmethod
    def get_count_for_article(article_id):
        """
        Get the total count for a single article
        """
        favorites_count = Favorite.objects.filter(
            article=article_id).count()
        return favorites_count

    @staticmethod
    def is_article_in_user_favorites(article_id, user_id):
        """
        Check if an article is already in user favorites
        """
        result = Favorite.objects.filter(article=article_id,
                                         user=user_id).exists()
        return result
