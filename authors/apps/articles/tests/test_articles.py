from .base_test import ArticleTestBase

from rest_framework import status


class TestArticle(ArticleTestBase):

    def test_create_article(self):
        """
        User should be able to create an article
        """
        self.authorize_user(self.user)
        response = self.client.post(self.articles_url, self.article, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) 
