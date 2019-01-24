from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
import jwt
from django.conf import settings


class TestBase(APITestCase):
    """
    Base class to set up basic variables and methods for authentication
    """

    def setUp(self):
        """Initialize variables and methods used by the tests."""
        self.user = {
            "user": {
                "username": "lolisme",
                "email": "lolisme2016@gmail.com",
                "password": "manu232#$$"
            }
        }
        self.user1 = {
            "user": {
                "username": "roboticstia",
                "email": "roboticstia@gmail.com",
                "password": "manu232#$$"
            }
        }

        self.client = APIClient()
        self.login_url = reverse('authentication:login_url')
        self.register_url = reverse('authentication:register_url')
        self.resend_url = reverse('authentication:resend_email_url')
        self.forgot_password_url = reverse('authentication:forgot_password')
        self.password_reset_token = self.get_password_reset_token()
        self.reset_password_url = reverse(
            'authentication:reset_password',
            kwargs={"token": self.password_reset_token})

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

        self.user_resend = {
            "user":{
                "email": "lolisme2016@gmail.com"
            }
        }

        self.username = {
            "user": {
                "username": "Jacob",
                "email": "lolisme2016@gmail.com",
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
        self.reset_password_payload = {
            "password": "Lolisme@2016",
            "confirm_password": "Lolisme@2016"
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

        self.user_reset_password = {
            "email": "lolisme2016@gmail.com",
            "password": "Lolisme@2016",
            "confirm_password": "Lolisme@2016"
        }

        self.user_resend_blank = {
            "user": {
                "email": ""
            }
        }

        self.user_resend_bad = {
            "user": {
                "email": "ioo@dn.com"
            }}
        self.user_login = {
            "user": {
                "email": "lolisme2016@gmail.com",
                "password": "manu232#$$"
            }
        }

    def register_user(self, data):
        return self.client.post(
            self.register_url,
            data,
            format='json'
        )

    def forgot_password_req(self, data):
        return self.client.post(
            self.forgot_password_url,
            data=data,
            format="json")

    def get_password_reset_token(self):
        response = self.register_user(self.user1)
        payload = response.data.get('user_info')
        token = jwt.encode({
            'email': payload['email'],
            'type': 'reset password'
        },
            settings.SECRET_KEY
        ).decode()
        return token

    def reset_password_req(self, data):
        return self.client.put(
            self.reset_password_url,
            data=data,
            format="json")

    def user_login_req(self, data):
        return self.client.post(
            self.login_url,
            data=data,
            format="json")
