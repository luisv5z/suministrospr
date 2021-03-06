from ckeditor.fields import RichTextField
from django.db import models
from django_extensions.db.fields import AutoSlugField

from ..utils.models import BaseModel
from .constants import MUNICIPALITIES


class Tag(BaseModel):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from=["name"], overwrite_on_add=False, max_length=255)

    def __str__(self):
        return self.name


class Municipality(BaseModel):
    MUNICIPALITY_CHOICES = [(value, label) for value, label in MUNICIPALITIES.items()]

    name = models.CharField(max_length=255, choices=MUNICIPALITY_CHOICES)
    slug = AutoSlugField(populate_from=["name"], overwrite_on_add=False, max_length=255)

    class Meta:
        verbose_name = "municipality"
        verbose_name_plural = "municipalities"

    def __str__(self):
        return self.name


class Suministro(BaseModel):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(
        populate_from=["title", "municipality"], overwrite_on_add=False, max_length=255
    )
    municipality = models.ForeignKey(
        Municipality,
        null=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name="suministros",
        related_query_name="suministro",
    )
    tags = models.ManyToManyField(Tag, blank=True)
    content = RichTextField()

    class Meta:
        indexes = [models.Index(fields=["title"])]
        verbose_name = "suministro"
        verbose_name_plural = "suministros"

    def __str__(self):
        return self.title
