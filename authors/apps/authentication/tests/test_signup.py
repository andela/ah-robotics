from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
import json


class TestUserRegistration(APITestCase):

    def setUp(self):
        self.url = reverse('authentication:signup')
        self.user = {
            'user': {
                'username': 'meshack',
                'email': 'meshack@gmail.com',
                'password': 'pass'
            }
        }
        self.register_user_success = {
            "user": {
                "email": "test@live.com",
                "password": "manu202@$3",
                "username": "testuser"
            }
        }
        self.user_mail = {
            'user': {
                'username': 'name',
                'email': 'meshack@mail',
                'password': 'pass'
            }
        }

    def test_password_should_not_be_less_than_8_characters(self):
        """
        test whether the user is successfully registered
        """
        response = self.client.post(self.url, self.user, format='json')
        response_message = json.loads(response.content)[
            "errors"]["password"][0]
        self.assertEqual(
            response_message,
            "Ensure this field has at least 8 characters.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_email_should_be_valid(self):
        """
        test whether the user email is valid
        """
        self.user["user"]["email"] = "mesh@d"
        response = self.client.post(self.url, self.user, format='json')
        response_message = json.loads(response.content)["errors"]["email"][0]
        self.assertEqual(
            response_message,
            "Enter a valid email address.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_that_password_is_alphanumeric(self):
        """
        test whether password entered has alphanumeric characters
        """
        self.user["user"]["password"] = "rtyhughg"
        response = self.client.post(self.url, self.user, format='json')
        response_message = json.loads(response.content)[
            "errors"]["password"][0]
        self.assertEqual(
            response_message,
            "Password must have letters, numbers and special characters")

        response = self.client.post(self.url, self.user_mail, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_success(self):
        """
        test whether the user has been registered successfully
        """

        response = self.client.post(
            self.url, self.register_user_success, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_exists(self):
        """
        test whether the user already exists
        """

        self.client.post(self.url, self.register_user_success, format='json')
        response = self.client.post(
            self.url, self.register_user_success, format='json')
        response_message = json.loads(response.content)["errors"]["email"][0]
        self.assertEqual(
            response_message,
            "user with this email already exists.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
