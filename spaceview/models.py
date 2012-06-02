from django.db import models

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType


class NamespaceAware(models.Model):
    """
    An abstract model to use on models you want to make space-aware.
    """
    
    space_content_type = models.ForeignKey(ContentType, blank=True, null=True)
    space_content_id = models.PositiveIntegerField(blank=True, null=True)
    space = generic.GenericForeignKey(ct_field="space_content_type", fk_field="space_content_id")
    
    class Meta:
        abstract = True
