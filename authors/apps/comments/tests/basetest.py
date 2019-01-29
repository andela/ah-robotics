from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from django.utils.text import slugify


class BaseTest(APITestCase):
    """
    Write reusable tests code here
    """

    def setUp(self):
        """
        Setup code that runs avery time a test executes
        """
        self.client = APIClient()
        self.registration_url = reverse('authentication:register_url')
        self.login_url = reverse('authentication:login_url')
        self.articles_url = reverse('articles:articles')

        self.sample_user = {
            "user": {
                "username": "shark",
                "email": "shark@gmail.com",
                "password": "Shark@2019"
            }
        }
        self.sample_bad_user = {
            "user": {
                "username": "sharky",
                "email": "sharky@gmail.com",
                "password": "Sharky@2019"
            }
        }

        self.sample_comment = {
            "comment": {
                "body": "I am a patcherian"
            }
        }

        self.sample_update_data = {
            "comment": {
                "body": "I a patcherian"
            }
        }

        self.sample_null_comment = {
            "comment": {
                "body": ""
            }
        }

        self.sample_article = {
            "article": {
                "title": "My Article",
                "description": "This is my article",
                "body": "This article was creeated by me",
                "tagList": ['test'],
                "author": 1
            }
        }

    def comment_url(self, slug):
        """
        Generate the urls
        """
        url = "/api/v1/articles/{}/comments/".format(slug)
        return url

    def authenticate_user(self, user):
        """
        Register and login a user
        """
        self.client.post(
            self.registration_url,
            user,
            format='json'
        )
        response = self.client.post(
            self.login_url,
            user,
            format='json'
        )
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='token ' + token)

    def create_article(self, article):
        """
        Create an article to be used in the tests
        """
        self.client.post(self.articles_url, article, format='json')

    def create_comment(self, comment_data, article):
        """
        A function to create a comment
        """
        return self.client.post(
            self.comment_url(slugify(article['article']['title'])),
            comment_data,
            format='json'
        )
