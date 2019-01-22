from rest_framework import status

from .base_test import TestBase


class TestEmailVerification(TestBase):
    """test whether a user receives a verification email on signup"""

    def test_an_email_is_sent_on_registration(self):
        """register a user"""
        response = self.register_user(data=self.user)
        self.assertEqual(response.data['message'],
            'User registered successfully. Check your email to activate your account.')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_email_verified(self):
        """Test whether the email gets verified successfully"""
        response = self.register_user(data=self.user)
        token = response.data['user_info']['token']
        self.verification_link = "/api/v1/users/verify/{}".format(token)
        resp = self.client.get(self.verification_link)
        self.assertEqual(resp.data, 'Email verification successful.')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)