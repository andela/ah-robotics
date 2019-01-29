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
        response = self.create_comment(self.sample_comment)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "Comment Successfully created")

    def test_unauthenticated_user_cannot_comment(self):
        """
        Tests whether a user who is unauthorized can comment
        """
        response = self.create_comment(self.sample_comment)
        self.create_article(self.sample_article)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], "You must be logged in to comment")
    
    def test_user_cannot_submit_empty_comment(self):
        """
        Ensure that all comments have data to submit
        """
        self.authenticate_user(self.sample_user)
        self.create_article(self.sample_article)
        response = self.create_comment(self.sample_null_comment)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "Comment Successfully created")

    def test_get_all_comments(self):
        """
        Test retrieve all comments
        """
        self.authenticate_user(self.sample_user)
        self.create_article(self.sample_article)
        self.create_comment(self.sample_comment)
        response = self.client.get(self.all_comments_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_comment(self):
        """
        Test retrieve one comment
        """
        self.authenticate_user(self.sample_user)
        self.create_article(self.sample_article)
        self.create_comment(self.sample_comment)
        response = self.client.get(self.one_comment_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_comment(self):
        """
        Test a user can update their comment
        """
        self.authenticate_user(self.sample_user)
        self.create_article(self.sample_article)
        self.create_comment(self.sample_comment)
        response = self.client.put(
            self.comment_update_url, 
            self.sample_update_data, 
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'],"Successfully updated")

    def test_unauthorized_update_comment(self):
        """
        Test a user cannot update other user's comment
        """
        self.authenticate_user(self.sample_user)
        self.create_article(self.sample_article)
        self.create_comment(self.sample_comment)
        self.authenticate_user(self.sample_bad_user)
        response = self.client.put(
            self.comment_update_url, 
            self.sample_update_data, 
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data['message'],
            "You are not authorized to edit this comment"
        )

    def test_delete_comment(self):
        """
        Test that a user can delete a comment
        """
        self.authenticate_user(self.sample_user)
        self.create_article(self.sample_article)
        self.create_comment(self.sample_comment)
        response = self.client.delete(self.one_comment_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_delete_comment(self):
        """
        Test that a user cannot delete another user's comment
        """
        self.authenticate_user(self.sample_user)
        self.create_article(self.sample_article)
        self.create_comment(self.sample_comment)
        self.authenticate_user(self.sample_bad_user)
        response = self.client.delete(self.one_comment_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data['message'],
            "You are not authorized to delete this comment"
        )


      

