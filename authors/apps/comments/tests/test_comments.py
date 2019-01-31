from .basetest import BaseTest
from rest_framework import status


class TestComments(BaseTest):
    """
    Comments Testcase
    """

    def test_create_comment(self):
        """
        Test whether a user can create a comment
        """
        self.authenticate_user(self.sample_user)
        self.create_article(self.sample_article)
        response = self.create_comment(
            self.sample_comment, self.sample_article)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauthenticated_user_cannot_comment(self):
        """
        Tests whether a user who is unauthorized can comment
        """
        self.create_article(self.sample_article)
        response = self.create_comment(
            self.sample_comment, self.sample_article)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'],
                         "Authentication credentials were not provided.")

    def test_user_cannot_submit_empty_comment(self):
        """
        Ensure that all comments have data to submit
        """
        self.authenticate_user(self.sample_user)
        self.create_article(self.sample_article)
        response = self.create_comment(
            self.sample_null_comment, self.sample_article)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['errors']["body"][0], "This field may not be blank.")

    def test_get_all_comments(self):
        """
        Test retrieve all comments
        """
        self.authenticate_user(self.sample_user)
        self.create_article(self.sample_article)
        self.create_comment(
            self.sample_comment, self.sample_article)
        response = self.client.get(self.comment_url("my-article"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_comment(self):
        """
        Test retrieve one comment
        """
        self.authenticate_user(self.sample_user)
        self.create_article(self.sample_article)
        res = self.create_comment(
            self.sample_comment, self.sample_article)
        url = self.comment_url("my-article")+'3/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_comment(self):
        """
        Test a user can update their comment
        """
        self.authenticate_user(self.sample_user)
        self.create_article(self.sample_article)
        res = self.create_comment(
            self.sample_comment, self.sample_article)

        url = self.comment_url("my-article")+'5/'
        response = self.client.put(
            url,
            self.sample_update_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauthorized_update_comment(self):
        """
        Test a user cannot update other user's comment
        """
        self.authenticate_user(self.sample_user)
        self.create_article(self.sample_article)
        self.create_comment(
            self.sample_comment, self.sample_article)
        self.authenticate_user(self.sample_bad_user)
        url = self.comment_url("my-article")+'5/'
        response = self.client.put(
            url,
            self.sample_update_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['comment']
                         ['message'], "Comment not found")
