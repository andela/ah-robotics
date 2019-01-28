from .base_test import TestBase
from rest_framework import status


class ProfilesTestCase(TestBase):
    """Test the user profile feature"""

    def test_that_a_user_profile_was_created_successfully(self):
        """Test whether the user profile is actually created"""
        response = self.register_user(data=self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_view_a_user_profile(self):
        """View one user's profile"""
        self.authorize_user(self.user_login_details)
        url = self.profiles_url + \
            '{}'.format(self.user['user']['username']) + "/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_all_users_profiles(self):
        """Test that a user can view all user profiles"""
        self.authorize_user(self.user_login_details)
        response = self.client.get(self.profiles_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_that_a_user_can_edit_their_profile(self):
        """Tests the edit profile functionality"""
        self.authorize_user(self.user_login_details)
        url = self.profiles_url + \
            '{}'.format(self.user['user']['username']) + "/"
        response = self.client.patch(url, data=self.user_bio)
        self.assertEqual(response.data['bio'], "You are a peculiar man.")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_that_a_user_cannot_edit_another_users_profile(self):
        """Tests that a user can only edit their profile"""
        self.authorize_user(self.user_login_details)
        self.register_user(self.user2)
        url = self.profiles_url + \
            '{}'.format(self.user2['user']['username']) + "/"
        response = self.client.patch(url, data=self.user_bio)
        message = "You don't have permission to edit this profile"
        self.assertEqual(response.data['message'], message)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
