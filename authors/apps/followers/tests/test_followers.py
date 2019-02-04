from rest_framework import status

from authors.apps.followers.tests.base_test import FollowerBaseTest


class FollowerTestCase(FollowerBaseTest):
    """
    Test Class containing tests for Favorite Module
    """
    def test_follow_without_auth(self):
        """
        Users should not be able to follow another user without
        being logged in
        """
        response = self.client.post(self.follow_url, format='json')
        self.assertEqual(response.data['detail'],
                         "Authentication credentials were not provided.")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_follow_with_auth(self):
        """
        User should be able to follow another user once they are 
        logged in
        """
        self.authorize_user(self.user)
        self.register_user(self.user2)
        response = self.client.post(self.follow_url, format='json')
        self.assertEqual(response.data['message'],
                         "user followed successfully")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_follow_non_existent_user(self):
        """
        User cannot follow non existent user
        """
        self.authorize_user(self.user)
        response = self.client.post(self.follow_url, format='json')
        self.assertEqual(response.data['error'],
                         "user with that name was not found")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_follow_self(self):
        """
        User cannot follow themselves
        """
        self.authorize_user(self.user)
        response = self.client.post(self.follow_self_url, format='json')
        self.assertEqual(response.data['error'],
                         "you cannot follow yourself.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_already_followed(self):
        """
        User cannot follow another user twice
        """
        self.authorize_user(self.user)
        self.register_user(self.user2)
        self.client.post(self.follow_url, format='json')
        response2 = self.client.post(self.follow_url, format='json')
        self.assertEqual(response2.data['error'],
                         "user already followed")
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unfollow_non_existent_user(self):
        """
        User cannot unfollow a non existent user
        """
        self.authorize_user(self.user)
        response = self.client.delete(self.unfollow_url,
                                      data=self.followed_user, format='json')
        self.assertEqual(response.data['error'],
                         'user not found')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unfollow_user_successfully(self):
        """
        User should be able to unfollow a user successfully
        """
        self.authorize_user(self.user)
        self.register_user(self.user2)
        self.client.post(self.follow_url, format='json')
        response = self.client.delete(self.unfollow_url,
                                      data=self.followed_user)
        self.assertEqual(response.data['message'],
                         'user unfollowed')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unfollow_user_without_auth(self):
        """
        User cannot unfollow another user if he/she are not
        logged in
        """
        self.register_user(self.user2)
        self.client.post(self.follow_url, format='json')
        response = self.client.delete(self.unfollow_url,
                                      data=self.followed_user)
        self.assertEqual(response.data['detail'],
                         "Authentication credentials were not provided.")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_list_of_following_users_with_auth(self):
        """
        User can get a list of users that he is currently following
        """
        self.authorize_user(self.user)
        self.register_user(self.user2)
        self.client.post(self.follow_url, format='json')
        response = self.client.get(self.following_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_of_following_users_withoutauth(self):
        """
        User should not get a list of users that he is
        currently following without authentication
        """
        response = self.client.get(self.following_list_url)
        self.assertEqual(response.data['detail'],
                         "Authentication credentials were not provided.")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

