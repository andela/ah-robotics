from .base_test import ArticleTestBase

from rest_framework import status


class TestArticle(ArticleTestBase):

    def test_add_article(self):
        """
        User should be able to add an article
        """
        self.authorize_user(self.user)
        response = self.post_article_req(self.article)
        created_slug = response.data['slug']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(created_slug, "the-one")

    def test_add_article_no_title_field(self):
        """
        User should not be able to add an article without a title field
        """
        self.article['article'].pop('title')
        self.authorize_user(self.user)
        response = self.post_article_req(self.article)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_message = response.data["errors"]["title"][0]
        self.assertEqual(response_message, "article title cannot be empty")

    def test_add_article_no_body_field(self):
        """
        User should not be able to add an article without a body field
        """
        self.article['article'].pop('body')
        self.authorize_user(self.user)
        response = self.post_article_req(self.article)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_message = response.data["errors"]["body"][0]
        self.assertEqual(response_message, "article body cannot be empty")

    def test_add_article_empty_title(self):
        """
        User should not be able to add an article with blank title field
        """
        self.authorize_user(self.user)
        response = self.post_article_req(self.article_empty_title)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_message = response.data["errors"]["title"][0]
        self.assertEqual(response_message, "This field may not be blank.")

    def test_add_article_empty_body(self):
        """
        User should not be able to add an article with blank body field
        """
        self.authorize_user(self.user)
        response = self.post_article_req(self.article_empty_body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_message = response.data["errors"]["body"][0]
        self.assertEqual(response_message, "This field may not be blank.")

    def test_add_article_unauthorized(self):
        """
        Unauthorized user should not be able to create an article
        """
        response = self.post_article_req(self.article)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response_message = response.data["detail"]
        self.assertEqual(response_message,
                         "Authentication credentials were not provided.")

    def test_view_single_article(self):
        """
        User should be able to view a single article
        """
        self.authorize_user(self.user)
        response = self.post_article_req(self.article)
        article_slug = response.data['slug']
        response2 = self.client.get(self.articles_url + article_slug + '/')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_view_single_article_unauthorized(self):
        """
        Unauthorized user should be able to view a single article
        """
        self.authorize_user(self.user)
        response = self.post_article_req(self.article)
        article_slug = response.data['slug']
        self.client.credentials()
        response2 = self.client.get(self.articles_url + article_slug + '/')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_view_articles_not_logged_in(self):
        """
        User not logged in should still be able to view articles
        """
        response = self.client.get(self.articles_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_articles_logged_in(self):
        """
        Logged in user should be able to view articles
        """
        self.authorize_user(self.user)
        response = self.client.get(self.articles_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_article_nonexistent(self):
        """
        User cannot view an article that does not exist
        """
        self.authorize_user(self.user)
        response = self.client.get(self.articles_url + "no-article-with-slug/",
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_message = response.data["errors"]["error"]
        self.assertEqual(response_message,
                         "No article found for the slug given")

    def test_update_article(self):
        """
        User should be able to update an existing article
        """
        self.authorize_user(self.user)
        response = self.post_article_req(self.article)
        article_slug = response.data['slug']
        response2 = self.client.put(self.articles_url + article_slug + '/',
                                    self.article_update_details, format='json')
        updated_title = response2.data["title"]
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_title, "The Updated One")

    def test_update_article_unauthorized(self):
        """
        Unauthorized user should not be able to update existing article
        """
        self.authorize_user(self.user)
        response = self.post_article_req(self.article)
        article_slug = response.data['slug']
        self.client.credentials()
        response2 = self.client.put(self.articles_url + article_slug + '/',
                                    self.article_update_details, format='json')
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)
        response_message = response2.data["detail"]
        self.assertEqual(response_message,
                         "Authentication credentials were not provided.")

    def test_delete_article(self):
        """
        User should be able to delete articles
        """
        self.authorize_user(self.user)
        response = self.post_article_req(self.article)
        article_slug = response.data['slug']
        response2 = self.client.delete(self.articles_url + article_slug + '/')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        response_message = response2.data["message"]
        self.assertEqual(response_message,
                         "article deleted successfully")

    def test_delete_article_unauthorized(self):
        """
        This method tests if a non owner can delete an article
        """
        self.authorize_user(self.user)
        response = self.post_article_req(self.article)
        article_slug = response.data['slug']
        self.client.credentials()
        response2 = self.client.delete(self.articles_url + article_slug + '/')
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)
        response_message = response2.data["detail"]
        self.assertEqual(response_message,
                         "Authentication credentials were not provided.")

    def test_add_tag_article(self):
        """
        User should be able to add tags to an article
        """
        self.authorize_user(self.user)
        response = self.client.post(self.articles_url,
                                    self.article, format='json')
        created_slug = response.data['slug']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(created_slug, "the-one")
        self.assertEqual(len(response.data["tagList"]), 3)
