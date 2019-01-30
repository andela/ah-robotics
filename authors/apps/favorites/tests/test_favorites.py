from .base_test import FavoriteTestBase

from rest_framework import status


class FavoriteTestCase(FavoriteTestBase):
    """
    Test Class containing tests for Favorite Module
    """

    def test_favorite_own_article(self):
        """
        User should be able to favorite his/her article
        """
        expected_message = 'article added to favorites'
        self.authorize_user(self.user)
        self.client.post(self.articles_url,
                         self.article, format='json')

        response = self.client.post(self.favorites_url,
                                    self.article_slug, format='json')
        message = response.data['message']

        self.assertEqual(expected_message, message)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_favorite_another_article(self):
        """
        User should be able to favorite another user's article
        """
        expected_message = 'article added to favorites'
        self.authorize_user(self.user)
        self.client.post(self.articles_url,
                         self.article, format='json')

        self.client.credentials()
        self.authorize_user(self.second_user)
        response = self.client.post(self.favorites_url,
                                    self.article_slug, format='json')
        message = response.data['message']

        self.assertEqual(expected_message, message)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_favorite_article_twice(self):
        """
        User should not be able to favorite an article more than once
        """
        expected_message = 'article already exists in favorites'
        self.authorize_user(self.user)
        self.client.post(self.articles_url,
                         self.article, format='json')

        self.client.post(self.favorites_url,
                         self.article_slug, format='json')

        response2 = self.client.post(self.favorites_url,
                                     self.article_slug, format='json')
        message = response2.data['error']
        self.assertEqual(expected_message, message)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_favorite_non_existent_article(self):
        """
        User should not be able to favorite an article
        that does not exist
        """
        expected_message = 'article with given slug not found'
        self.authorize_user(self.user)
        self.client.post(self.articles_url,
                         self.article, format='json')

        response = self.client.post(self.favorites_url,
                                    self.absent_article_slug, format='json')
        message = response.data['error']

        self.assertEqual(expected_message, message)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_article_from_favorites(self):
        """
        User should be able to remove an article from favorites
        """
        expected_message = 'article removed from favorites'
        self.authorize_user(self.user)
        self.client.post(self.articles_url,
                         self.article, format='json')
        self.client.post(self.favorites_url,
                         self.article_slug, format='json')

        response = self.client.delete(self.favorites_url
                                      + self.existing_article_slug
                                      + '/')
        message = response.data['message']
        self.assertEqual(expected_message, message)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_article_from_favorites_twice(self):
        """
        User should not be able to remove an article
        from favorites more than once
        """
        expected_message = 'article not in favorites'
        self.authorize_user(self.user)
        self.client.post(self.articles_url,
                         self.article, format='json')
        self.client.post(self.favorites_url,
                         self.article_slug, format='json')
        self.client.delete(self.favorites_url
                           + self.existing_article_slug
                           + '/')

        response = self.client.delete(self.favorites_url
                                      + self.existing_article_slug
                                      + '/')
        message = response.data['message']
        self.assertEqual(expected_message, message)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_non_existent_article_favorites(self):
        """
        User should not be able to delete a favorite
        article that does not exist
        """
        expected_message = 'article with given slug not found'
        self.authorize_user(self.user)
        self.client.post(self.articles_url,
                         self.article, format='json')

        response = self.client.delete(self.favorites_url
                                      + self.non_existent_article_slug
                                      + '/')
        message = response.data['error']

        self.assertEqual(expected_message, message)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
