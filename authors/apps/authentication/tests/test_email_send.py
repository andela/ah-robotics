from django.urls import reverse
from rest_framework import status
from .base_test import TestBase
from django.contrib.auth.tokens import default_token_generator
from authors.apps.authentication.models import User


class ForgotPasswordTestCase(TestBase):
    """Test that email is sent to a user"""

    def test_unregistered_email(self):
        """
        Test that unregistered user cannot receive email
        """
        response = self.forgot_password_req(
            data={"email": self.user['user']['email']})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.content,
            b'["Account with the email does not exist."]')

    def test_empty_email_payload(self):
        """
        Test if email can be sent without providing email
        """
        response = self.forgot_password_req(
            data={"email": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.content,
            b'["Account with the email does not exist."]')

    def test_user_with_valid_email(self):
        """
        Tests if valid and registered user will receive email
        """
        register_user = self.register_user(data=self.user)
        self.assertEqual(
            register_user.data['user_info']['email'], self.user['user']['email'])
        self.assertEqual(register_user.status_code, status.HTTP_201_CREATED)
        response = self.forgot_password_req(
            data={"email": self.user['user']['email']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ResetPasswordTestcase(TestBase):
    """Test if a registered user can reset their password"""

    # def test_password_reset_valid_password(self):
    #     """Test that a user with valid credentials can reset password"""
    #     response = self.reset_password_req(data=self.reset_password_payload)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_passwords_not_matching(self):
        """Test that user cannot reset password with unmatching password"""
        self.user_reset_password['password'] = "pass123@4"
        self.user_reset_password['confirm_password'] = "bad pass"
        response = self.reset_password_req(data=self.user_reset_password)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_password(self):
        self.user_reset_password['password'] = "bad pass"
        response = self.reset_password_req(data=self.user_reset_password)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_empty_password(self):
        self.user_reset_password['password'] = " "
        response = self.reset_password_req(data=self.user_reset_password)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
