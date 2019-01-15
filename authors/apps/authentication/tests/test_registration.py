from rest_framework import status

from .base_test import TestBase


class TestRegister(TestBase):
    """User registration test case"""

    def test_register_user(self):
        """Test to register a user."""

        response = self.register_user(data=self.user)
        self.assertEqual(response.data['email'], 'jake@jake.jake')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_wrong_email_format(self):
        """Test to register a user."""

        response = self.register_user(data=self.user_wrong_email_format)
        self.assertEqual(
            response.data['errors']['email'][0],
            "Enter a valid email address.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_email(self):
        """Test for registration of a duplicate email."""

        response = self.register_user(data=self.user)
        response_duplicate_url = self.register_user(data=self.user)
        self.assertEqual(
            response_duplicate_url.data['errors']['email'][0],
            "user with this email already exists.")
        self.assertEqual(response_duplicate_url.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_duplicate_username(self):
        """Test for registration of a duplicate username."""

        response = self.register_user(data=self.username)
        response_duplicate_url = self.register_user(data=self.username1)
        self.assertEqual(
            response_duplicate_url.data['errors']['username'][0],
            "user with this username already exists.")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_duplicate_url.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_register_user_no_email(self):
        """Test for registration of a user without email."""

        response = self.register_user(data=self.user_no_email)
        self.assertEqual(
            response.data['errors']['email'][0],
            "This field may not be blank.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_no_username(self):
        """Test for registration of a user without username."""

        response = self.register_user(self.user_no_username)
        self.assertEqual(
            response.data['errors']['username'][0],
            "This field may not be blank.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_empty_password(self):
        """This is the test for register with empty password."""

        response = self.register_user(data=self.user_no_password)
        self.assertEqual(
            response.data['errors']['password'][0],
            "This field may not be blank.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_empty_payload(self):
        """This is the test for register with empty password."""

        response = self.register_user(data=self.empty_payload)
        self.assertEqual(response.data['errors']
                         ['username'][0], "This field is required.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
