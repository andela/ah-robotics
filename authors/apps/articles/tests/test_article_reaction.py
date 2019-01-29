from .base_test import BaseReactionTestCase
from rest_framework import status


class ArticleLikeTestCase(BaseReactionTestCase):
    def test_user_can_like_an_article(self):
        """
        login and authorize user
        """
        self.authorize_user(self.user)
        response = self.client.post(self.like_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], True)

    def test_unauthenticated_user_can_not_like(self):
        """
        clear the authorization header
        """
        self.client.credentials()
        response = self.client.post(self.like_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'],
                         "Authentication credentials were not provided.")

    def test_article_can_have_many_likes(self):
        """
        first like from the first user
        """
        self.authorize_user(self.user)
        response = self.client.post(self.like_url, format="json")
        self.assertEqual(response.data['likes'], 1)
        """
        second like from the second user
        """
        self.authorize_user(self.user1)
        response = self.client.post(self.like_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['likes'], 2)

    def test_liking_revokes_dislike(self):
        self.authorize_user(self.user)
        response = self.client.post(self.dislike_url, format="json")  # dislike
        self.assertEqual(response.data['dislikes'], 1)
        response = self.client.post(self.like_url, format="json")  # like
        self.assertEqual(response.data['dislikes'], 0)


class ArticleDislikeTestCase(BaseReactionTestCase):
    def test_user_can_dislike_an_article(self):
        """
        login and authorize user
        """
        self.authorize_user(self.user)
        response = self.client.post(self.dislike_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], True)

    def test_unauthenticated_user_can_not_dislike(self):
        """
        clear the authorization header
        """
        self.client.credentials()
        response = self.client.post(self.dislike_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'],
                         "Authentication credentials were not provided.")

    def test_article_can_have_many_dislikes(self):
        """
        first dislike from the first user
        """
        self.authorize_user(self.user)
        response = self.client.post(self.dislike_url, format="json")
        self.assertEqual(response.data['dislikes'], 1)
        """
        second dislike from the second user
        """
        self.authorize_user(self.user1)
        response = self.client.post(self.dislike_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['dislikes'], 2)

    def test_disliking_revokes_like(self):
        self.authorize_user(self.user)
        response = self.client.post(self.like_url, format="json")  # like
        self.assertEqual(response.data['likes'], 1)
        response = self.client.post(
            self.dislike_url, format="json")  # dislike
        self.assertEqual(response.data['likes'], 0)
