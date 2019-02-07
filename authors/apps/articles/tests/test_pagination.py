from .base_test import ArticleTestBase

from rest_framework import status


class TestPagination(ArticleTestBase):
    """
    Test the pagination of articles
    """

    def test_total_article_count(self):
        """
        User should be able to get the total number of
        articles in the application
        """
        self.authorize_user(self.user)
        self.post_several_articles(20)

        response = self.client.get(self.articles_url)

        article_count = response.data["count"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(article_count, 20)

    def test_if_next_page_exists(self):
        """
        User should be able to get a url link to the next page
        if article number exceeds page maximum
        """
        self.authorize_user(self.user)
        self.post_several_articles(20)

        response = self.client.get(self.articles_url)
        next_page_url = response.data["next"]

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(next_page_url is None, False)
