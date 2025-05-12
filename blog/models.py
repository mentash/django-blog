from django.conf import settings
from django.db import models
from django.utils import timezone
from django.db.models.functions import Now

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey( # many-to-one
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts', # author.blog_posts
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    # Use database-computed default values using database function
    # publish = models.DateTimeField(db_default=Now())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=2,
        choices=Status.choices, # [('DF', 'Draft'), ('PB', 'Published')]
        default=Status.DRAFT,
    )

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]


    def __str__(self):
        return self.title

