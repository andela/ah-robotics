from django.db import models


class TimestampMixin(models.Model):
    """
    This model creates created_at and updated_at fields
    """
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        """
        make the model to prevent default migration but instead adds
        created_at and updated_at fields to other models which
        inherits this model
        """
        abstract = True
        # defines the ordering of the model by the create_at field
        ordering = ['-created_at', '-updated_at', '-id']
