from django.urls import reverse

from rest_framework.test import APITestCase, APIClient


class FavoriteTestBase(APITestCase):
    """
    This is the base test class that shall be inherited by favorite test files
    """

    def setUp(self):
        """Set up configurations that shall be run every time a test runs"""
        self.user = {
            "user": {
                "username": "tester",
                "email": "tester123@gmail.com",
                "password": "tester232#$$"
            }
        }
        self.second_user = {
            "user": {
                "email": "tester123@gmail.com",
                "password": "tester232#$$"}
        }
        self.article = {
            "article": {
                "title": "The One",
                "description": "This is an article about the one",
                "body": "The one is the one",
                "tagList": ["sample", "article"],
                "author": 1}
        }
        self.article_slug = {
            "article_slug": "the-one"
        }
        self.absent_article_slug = {
            "article_slug": "article-absent"
        }
        self.existing_article_slug = "the-one"
        self.non_existent_article_slug = "article-absent"
        self.client = APIClient()
        self.register_url = reverse('authentication:register_url')
        self.login_url = reverse('authentication:login_url')
        self.articles_url = reverse('articles:articles')
        self.favorites_url = reverse('favorites:favorites')

    def register_user(self, data):
        return self.client.post(
            self.register_url,
            data,
            format='json'
        )

    def login_a_user(self, data):
        return self.client.post(
            self.login_url,
            data,
            format='json'
        ).data

    def authorize_user(self, user_login_details):
        """
        Obtain token for access to protected endpoints
        """
        self.register_user(data=self.user)
        payload = self.login_a_user(data=user_login_details)
        self.client.credentials(HTTP_AUTHORIZATION='token ' + payload['token'])
