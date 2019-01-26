from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
import jwt
from django.conf import settings
import json


class ArticleTestBase(APITestCase):
    """
    This is a general class that shall be inherited by all test files
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
        self.user_login_details = {
            "user": {
                "email": "tester123@gmail.com",
                "password": "tester232#$$"

            }
        }
        self.article = {
            "article": {
                "title": "The One",
                "description": "This is an article about the one",
                "body": "The one is the one",
                "author": 1
            }
        }
        self.client = APIClient()
        self.register_url = reverse('authentication:register_url')
        self.login_url = reverse('authentication:login_url')
        self.articles_url = reverse('articles:articles')

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

    def authorize_user(self, user_details):
        # register a user
        self.register_user(data=self.user)
        payload = self.login_a_user(data=user_details)
        self.client.credentials(HTTP_AUTHORIZATION='token ' + payload['token'])
