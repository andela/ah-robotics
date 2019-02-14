from django.urls import reverse
from rest_framework import status
from .base_test import TestBase
from authors.apps.authentication.models import User


class ForgotPasswordTestCase(TestBase):
    """Test that email is sent to a user"""

    def test_sucess_user_login(self):
        """Test that a user can login successfully"""
        self.register_user(data=self.user)
        response = self.user_login_req(data=self.user_login)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], "lolisme2016@gmail.com")

    def test_login_unregistered_user(self):
        """Test that an unregistered user cannot login"""
        response = self.user_login_req(data=self.user_login)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors']['error'][0],
                         "Incorrect email or password.")

    def test_bad_email(self):
        """Test that a user cannot login with a bad email format"""
        self.register_user(data=self.user)
        self.user_login["user"]["email"] = "mail.com"
        response = self.user_login_req(data=self.user_login)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors']['error'][0],
                         "Incorrect email or password.")

    def test_wrong_pass(self):
        """Test that a user cannot login with the wrong password"""
        self.register_user(data=self.user)
        self.user_login["user"]["password"] = "bad_password"
        response = self.user_login_req(data=self.user_login)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors']['error'][0],
                         "Incorrect email or password.")
