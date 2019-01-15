from rest_framework import status
from .base_test import TestBase


class TestTokenGeneration(TestBase):
    """ Test token generation upon registration"""

    def test_token_generation_on_register(self):
        """ Test is token is returned after user registration"""
        response = self.register_user(self.user)
        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
