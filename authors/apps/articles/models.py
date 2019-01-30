from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager

from authors.apps.authentication.models import User
from authors.apps.core.models import TimestampMixin

from cloudinary.models import CloudinaryField


class Article(TimestampMixin, models.Model):
    """
    Model representation of an article
    """
    slug = models.SlugField(
        db_index=True, max_length=1000, unique=True, blank=True)
    title = models.CharField(max_length=500, blank=False)
    description = models.CharField(max_length=1000, blank=False)
    body = models.TextField(blank=False)
    image = CloudinaryField(blank=True, null=True)
    tagList = TaggableManager()
    author = models.ForeignKey(User,
                               related_name='article',
                               on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def generate_slug(self):
        """
        Generates a slug for article title
        Example: "Me is a me" is converted to "me-is-a-me"
        """
        slug = slugify(self.title)
        new_slug = slug
        n = 1
        while Article.objects.filter(slug=new_slug).exists():
            """increment slug value by one if already exists"""
            new_slug = '{}-{}'.format(slug, n)
            n += 1

        return new_slug

    def save(self, *args, **kwargs):
        """
        Create article and save to db
        """
        if not self.slug:
            self.slug = self.generate_slug()
        super().save(*args, **kwargs)
