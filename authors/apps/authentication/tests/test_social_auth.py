import json
import os
from django.urls import reverse
from rest_framework.views import status
from rest_framework.test import APITestCase, APIClient
from .base_test import TestBase


class SocialAuth(TestBase):
    """Test Social authentication"""

    def test_fails_invalid_provider_name(self):
        """Test invalid social authentication provider name."""
        response = self.social_login_req(self.invalid_provider)
        self.assertEqual(response.data['error'],
                         'Please provide a valid social provider')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fails_with_invalid_token(self):
        """Test that user cannot login with invalid google token"""
        response = self.social_login_req(self.google_provider)
        self.assertEqual(response.data['errors'],
                         'Invalid token')
