from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.db.models.functions import Now
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    tags = TaggableManager() # Use taggit for tagging posts
    slug = models.SlugField(
        max_length=250,
        unique_for_date='publish', # Slug must be unique for each publish-date
    )
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
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Custom manager for published posts.

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
        )

class Comment(models.Model):
    # Create relationship with Post model
    post = models.ForeignKey( # many-to-one relationship with Post model
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    # Create comment fields
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True) # Set only on creation
    updated = models.DateTimeField(auto_now=True) # Updated on every save
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'