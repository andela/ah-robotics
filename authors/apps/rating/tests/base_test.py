from django.urls import reverse
from rest_framework.test import APITestCase, APIClient


class RatingTestBase(APITestCase):
    """
    This is the base test class that shall be inherited by article test files
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
        self.user1 = {
            "user": {
                "username": "tester1",
                "email": "tester1234@gmail.com",
                "password": "tester232#$$"
            }
        }
        self.user_login_details = {
            "user": {
                "email": "tester123@gmail.com",
                "password": "tester232#$$"}
        }
        self.user_login_details1 = {
            "user": {
                "email": "tester1234@gmail.com",
                "password": "tester232#$$"}
        }
        self.article = {
            "article": {
                "title": "The One",
                "description": "This is an article about the one",
                "body": "The one is the one",
                "tagList": ["obi"],
                "author": 1}
        }
        self.rating = {
            "user_rating": 2
        }
        self.rating1 = {
            "user_rating": 5
        }
        self.client = APIClient()
        self.register_url = reverse('authentication:register_url')
        self.login_url = reverse('authentication:login_url')
        self.articles_url = reverse('articles:articles')
        self.register_user(self.user)
        self.register_user(self.user1)
        self.token1 = self.login_a_user(self.user_login_details)['token']
        self.token2 = self.login_a_user(self.user_login_details1)['token']

    def register_user(self, data):
        """register a user"""
        return self.client.post(self.register_url, data, format='json')

    def login_a_user(self, data):
        """Login a user"""
        return self.client.post(self.login_url, data, format='json').data

    def authorize_user(self, user_details):
        """Register and login user to obtain token"""
        self.register_user(data=self.user)
        payload = self.login_a_user(data=user_details)
        self.client.credentials(HTTP_AUTHORIZATION='token ' + payload['token'])

    def post_article_req(self, data):
        return self.client.post(
            self.articles_url,
            data=data,
            HTTP_AUTHORIZATION='token ' + self.token1,
            format="json")

