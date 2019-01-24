# from rest_framework.reverse import reverse
# from rest_framework import status
# from .base_test import TestBase
# # Import Article rating model as 'ArticleRating'

# class TestRatingArticle(TestBase):
#     """Tests for rating an article"""
#     def setUp(self):
#         """Set up test variables and methods"""
#         super.setUp()

#         """
#             Register user
#             Activate User
#             Login User
#             Get the Auth Token
#             Post an Article"""
#         self.register_user(data=self.user)
#         # verify user
#         # self.lo

#     def test_successful_article_rate(self):
#         """Test that an article is rated successfully"""

#         get_ratings_count = ArticleRating.objects.count()
#         response = self.post_article_req(data=self.article)
#         self.slug = response.data['slug'] 
#         self.rate_article_url = reverse(
#             'articles:rate', kwargs={"slug", self.slug})
#         self.post_article_req(data=self.article)
#         self.rate_article_req(data=self.rating)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(ArticleRating.objects.count(), get_ratings_count+1)

#     def test_article_rate_update(self):
#         """Test that a user can update a previous rating to an article"""
#         pass

#     def test_rating_own_article(self):
#         """Test that a user CANNOT rate their own article"""
#         pass

#     def test_unsucessful_rating_with_invalid_rating(self):
#         """Test that user cannot submit an invalid rating"""
#         pass

#     def test_unsucessful_rating_with_rating_greater_than_five(self):
#         """Test that user cannot submit a rating greater than five"""
#         pass

#     def test_rating_not_existing_article(self):
#         """Test that a user cannot rate a non-existent article"""
#         pass
