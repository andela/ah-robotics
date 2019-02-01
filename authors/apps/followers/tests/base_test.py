from django.urls import reverse

from rest_framework.test import APITestCase, APIClient


class FollowerBaseTest(APITestCase):
    """
    This is the base test class that shall be inherited by followers test files
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

        self.user2 = {
            "user": {
                "username": "paulotieno",
                "email": "paulotieno@gmail.com",
                "password": "tester232#$$"
            }
        }

        self.followed_user = {
            "username": "paulotieno"
        }

        self.non_existent_user = {
            "username": "jameswan"
        }

        self.follow_self = {
            "username": "tester"
        }

        self.client = APIClient()
        self.register_url = reverse('authentication:register_url')
        self.login_url = reverse('authentication:login_url')
        self.follow_url = reverse('followers:follow_url', kwargs={
            "username": self.followed_user['username']}
            )
        self.follow_self_url = reverse('followers:follow_url', kwargs={
            "username": self.follow_self['username']}
        )
        self.unfollow_url = reverse('followers:delete_url', kwargs={
            "username": self.followed_user['username']
        })
        self.following_list_url = reverse('followers:following_url')

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
