from rest_framework.reverse import reverse
from .base_test import BookmarkTestBase
from rest_framework import status
from ..models import BookmarkArticle


class TestBookmarkArticle(BookmarkTestBase):
    """Tests for bookmarking an article"""

    def test_non_existent_bookmarks(self):
        """ """
        response = self.client.get(
            self.bookmark_url,
            format='json',
            HTTP_AUTHORIZATION='token ' + self.token1
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'NO article Bookmarked')

    def test_non_existing_slug(self):
        """ Testing for non existent bookmarks"""
        slug = 'non_existing_article'
        bookmark_article_url = reverse('bookmark:bookmark-article',
                                       kwargs={
                                           'slug': slug
                                       })
        response = self.client.post(bookmark_article_url, format="json")
        self.assertEqual(response.data['errors']['error'],
                         'No article found for the slug given')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bookmark_toggle_feature(self):
        """ Test for toggle between mark and unmark bookmark"""
        response = self.post_article_req(self.article)
        slug = response.data['slug']
        url = reverse('bookmark:bookmark-article',
                      kwargs={
                          'slug': slug
                      })
        bookmark_response = self.client.post(url,
                                             HTTP_AUTHORIZATION='token ' +
                                             self.token1, format="json")
        self.assertEqual(bookmark_response.status_code,
                         status.HTTP_201_CREATED)
        self.assertEqual(bookmark_response.data['message'],
                         'Article succesfully BOOKMARKED')

        res_unmark = self.client.post(url,
                                      HTTP_AUTHORIZATION='token ' +
                                      self.token1, format="json")

        self.assertEqual(res_unmark.status_code, status.HTTP_200_OK)
        self.assertEqual(res_unmark.data['message'],
                         'Bookmark succesfully DELETED')
