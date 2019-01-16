from django.urls import reverse
from rest_framework.test import APITestCase, APIClient


class TestBase(APITestCase):
    """
    Base class to set up basic variables and methods for authentication
    """

    def setUp(self):
        """Initialize variables and methods used by the tests."""

        self.client = APIClient()
        self.login_url = reverse('authentication:login_url')
        self.register_url = reverse('authentication:register_url')

        self.user = {
            "user": {
                "username": "Jacob",
                "email": "jake@jake.jake",
                "password": "manu232#$$"
            }
        }

        self.empty_payload = {
            "user": {}
        }

        self.user_wrong_email_format = {
            "user": {
                "username": "Jacob",
                "email": "jakejakejake",
                "password": "manu232#$$"
            }
        }

        self.username = {
            "user": {
                "username": "Jacob",
                "email": "jake@jake.jake",
                "password": "manu232#$$"
            }
        }

        self.username1 = {
            "user": {
                "username": "Jacob",
                "email": "jake1@jake.jake",
                "password": "manu232#$$"
            }
        }
        self.user_no_email = {
            "user": {
                "username": "Jacob",
                "email": "",
                "password": "manu232#$$"
            }
        }
        self.user_no_username = {
            "user": {
                "username": "",
                "email": "jake@jake.com",
                "password": "manu232#$$"
            }
        }
        self.user_no_password = {
            "user": {
                "username": "jake",
                "email": "jake@jake.com",
                "password": ""
            }
        }

        self.user_short_password = {
            'user': {
                'username': 'meshack',
                'email': 'meshack@gmail.com',
                'password': 'pass'
            }
        }

        self.user_non_alphanumeric_password = {
            'user': {
                'username': 'meshack',
                'email': 'meshack@gmail.com',
                'password': 'passnjsnffsfn'
            }
        }

    def register_user(self, data):
        return self.client.post(
            self.register_url,
            data,
            format='json'
        )
