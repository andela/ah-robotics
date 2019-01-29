from rest_framework.reverse import reverse
from rest_framework import status
from authors.apps.rating.models import Rating as ArticleRating
from .base_test import RatingTestBase


class TestRatingArticle(RatingTestBase):
    """Tests for rating an article"""

    def test_successful_article_rate(self):
        """Test that an article is rated successfully"""

        get_ratings_count = ArticleRating.objects.count()
        response = self.post_article_req(data=self.article)
        self.slug = response.data['slug']
        self.rate_article_url = reverse(
            'rating:rating', kwargs={"slug": self.slug})
        self.post_article_req(data=self.article)
        rate_response = self.client.post(
            self.rate_article_url,
            data=self.rating,
            HTTP_AUTHORIZATION='token ' + self.token2,
            format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ArticleRating.objects.count(), get_ratings_count+1)
        self.assertEqual(
            rate_response.data['message'], 'Rating submitted sucessfully')

    def test_article_rate_update(self):
        """Test that a user can update a previous rating to an article"""
        response = self.post_article_req(data=self.article)
        self.slug = response.data['slug']
        self.rate_article_url = reverse(
            'rating:rating', kwargs={"slug": self.slug})
        self.post_article_req(data=self.article)
        rate_response = self.client.post(
            self.rate_article_url,
            data=self.rating,
            HTTP_AUTHORIZATION='token ' + self.token2,
            format="json")
        rate_response1 = self.client.post(
            self.rate_article_url,
            data=self.rating1,
            HTTP_AUTHORIZATION='token ' + self.token2,
            format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            rate_response.data['message'], 'Rating submitted sucessfully')
        self.assertEqual(
            rate_response1.data['message'], 'Rating submitted sucessfully')

    def test_rating_own_article(self):
        """Test that a user CANNOT rate their own article"""
        response = self.post_article_req(data=self.article)
        self.slug = response.data['slug']
        self.rate_article_url = reverse(
            'rating:rating', kwargs={"slug": self.slug})
        self.post_article_req(data=self.article)
        rate_response = self.client.post(
            self.rate_article_url,
            data=self.rating,
            HTTP_AUTHORIZATION='token ' + self.token1,
            format="json")
        self.assertEqual(rate_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            rate_response.data['message'], 'You cannot rate your own article')

    def test_unsucessful_rating_with_invalid_rating(self):
        """Test that user cannot submit an invalid rating such as a string"""
        response = self.post_article_req(data=self.article)
        self.slug = response.data['slug']
        self.rate_article_url = reverse(
            'rating:rating', kwargs={"slug": self.slug})
        self.post_article_req(data=self.article)
        self.rating['user_rating'] = ' '
        rate_response = self.client.post(
            self.rate_article_url,
            data=self.rating,
            HTTP_AUTHORIZATION='token ' + self.token2,
            format="json")
        self.assertEqual(
            rate_response.data['errors']['user_rating'][0], 'A valid integer is required.')

    def test_unsucessful_rating_with_rating_greater_than_five(self):
        """Test that user cannot submit a rating greater than five"""
        response = self.post_article_req(data=self.article)
        self.slug = response.data['slug']
        self.rate_article_url = reverse(
            'rating:rating', kwargs={"slug": self.slug})
        self.post_article_req(data=self.article)
        self.rating['user_rating'] = 100
        rate_response = self.client.post(
            self.rate_article_url,
            data=self.rating,
            HTTP_AUTHORIZATION='token ' + self.token2,
            format="json")
        self.assertEqual(
            rate_response.data['errors']['user_rating'][0], 'The maximum allowed rating is 5')

    def test_rating_not_existing_article(self):
        """Test that a user cannot rate a non-existent article"""

        self.rate_article_url = reverse(
            'rating:rating', kwargs={"slug": 'not_an_article'})
        rate_response = self.client.post(
            self.rate_article_url,
            data=self.rating,
            HTTP_AUTHORIZATION='token ' + self.token2,
            format="json")
        self.assertEqual(
            rate_response.data['errors']['message'], 'Article not found')
