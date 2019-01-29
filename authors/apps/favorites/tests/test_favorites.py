from .base_test import FavoriteTestBase

from rest_framework import status


class TestArticle(FavoriteTestBase):

    def test_favorite_article(self):
        """
        User should be able to favorite an article
        """
        self.authorize_user(self.user)
        response = self.client.post(self.articles_url,
                                    self.article, format='json')
        article_slug = response.data['slug']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(article_slug, "the-one")

        expected_message = 'article added to favorites'
        response2 = self.client.post(self.favorites_url,
                                     self.article_slug, format='json')
        message = response2.data['message']
        self.assertEqual(expected_message, message)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
