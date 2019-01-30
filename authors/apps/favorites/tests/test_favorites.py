from rest_framework import status

from .base_test import FavoriteTestBase, generate_slug_url


class FavoritesTestCase(FavoriteTestBase):
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

        response = self.client.put(
            generate_slug_url(self.article_slug))
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
        response = self.client.put(
            generate_slug_url(self.article_slug))
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

        self.client.put(generate_slug_url(self.article_slug))

        response = self.client.put(generate_slug_url(self.article_slug))
        message = response.data['error']
        self.assertEqual(expected_message, message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_favorite_non_existent_article(self):
        """
        User should not be able to favorite an article
        that does not exist
        """
        expected_message = 'article with given slug not found'
        self.authorize_user(self.user)
        self.client.post(self.articles_url,
                         self.article, format='json')

        response = self.client.put(
            generate_slug_url(self.non_existent_article_slug))
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
        self.client.put(
            generate_slug_url(self.article_slug))

        response = self.client.delete(
            generate_slug_url(self.article_slug))
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
        self.client.put(
            generate_slug_url(self.article_slug))
        self.client.delete(
            generate_slug_url(self.article_slug))

        response = self.client.delete(
            generate_slug_url(self.article_slug))
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

        response = self.client.delete(
            generate_slug_url(self.non_existent_article_slug))
        message = response.data['error']

        self.assertEqual(expected_message, message)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
