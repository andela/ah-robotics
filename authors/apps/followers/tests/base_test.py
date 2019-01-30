from django.urls import reverse
from rest_framework.test import APITestCase, APIClient


class FollowersTestBaseCase(APITestCase):
    """
    This is the base test class that shall be inherited by followers test files
    """
    def setUp(self):
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

        self.client = APIClient()
        self.register_url = reverse('authentication:register_url')
        self.login_url = reverse('authentication:login_url')
        self.followers_url = reverse('profiles:followers')
        self.following_url = reverse('profiles:following')
        