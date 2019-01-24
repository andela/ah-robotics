from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
import jwt
from django.conf import settings


class TestBase(APITestCase):
    """
    This is a general class that shall be inherited by all test files
    """

    def setUp(self):
        """Set up configurations that shall be run every time a test runs"""
        self.user = {
            "user": {
                "username": "lolisme",
                "email": "lolisme2016@gmail.com",
                "password": "manu232#$$"
            }
        }
        self.user_login_details = {
            "user": {
                "email": "lolisme2016@gmail.com",
                "password": "manu232#$$"

            }
        }
        self.bad_user_login = {
            "user": {
                "email": "2016@gmail.com",
                "password": "manu232#$$"

            }
        }
        self.client = APIClient()
        self.login_url = reverse('authentication:login_url')
        self.register_url = reverse('authentication:register_url')
        self.profiles_url = reverse('profiles:profiles')
        


    def register_user(self, data):
        return self.client.post(
            self.register_url,
            data,
            format='json'
        )
    def login_a_user(self,data):
        return self.client.post(
            self.login_url, 
            data, 
            format='json'
        ).data
    
    def edit_profile(self,username):
        self.one_profile_url = reverse(
            'profiles:username', 
            kwargs={"username":username}
        )
        return self.client.put(self.one_profile_url)
    
    def authorize_user(self,user_details):
        # register a user
        self.register_user(data=user_details)
        token = self.login_a_user(data=user_details)['token']
        self.client.credentials(HTTP_AUTHORIZATION= 'Bearer '+token)

    # def forgot_password_req(self, data):
    #     return self.client.post(
    #         self.forgot_password_url,
    #         data=data,
    #         format="json")

   