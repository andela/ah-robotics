from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager

from authors.apps.authentication.models import User
from authors.apps.core.models import TimestampMixin

from cloudinary.models import CloudinaryField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.db.models import Sum


class ReactionManager(models.Manager):
    """
    The class enables article likes and dislikes set to be managed separately.
    """
    use_related_fields = True

    def likes(self):
        """fetches reactions with a value greater than zero"""
        return self.get_queryset().filter(reaction__gt=0)

    def dislikes(self):
        """fetches reactions with a value less than zero"""
        return self.get_queryset().filter(reaction__lt=0)

    def sum_rating(self):
        """returns the sum of reaction items"""
        return self.get_queryset().aggregate(
            Sum('reaction')).get('reaction__sum') or 0


class Reaction(models.Model):
    LIKE = 1
    DISLIKE = -1
    """ reactions set contains either a like a dislike """
    REACTIONS = (
        (LIKE, 'like'),
        (DISLIKE, 'dislike')
    )
    """ reaction field can be set to a like or dislike """
    reaction = models.SmallIntegerField(choices=REACTIONS)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    """ defines the type of  related object """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    """ defines the object id for the related object """
    object_id = models.PositiveSmallIntegerField()
    """ provides generic foreign key using content_type and object_id """
    content_object = GenericForeignKey()

    objects = ReactionManager()


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
    reaction = GenericRelation(Reaction, related_query_name='article')

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
