from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    # Another pattern for establishing enumeration-style choices
    # https://docs.djangoproject.com/en/4.1/ref/models/fields/#enumeration-types
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT
    )

    # Django pattern: nested class for defining metadata
    # https://docs.djangoproject.com/en/4.1/topics/db/models/#meta-options
    # https://docs.djangoproject.com/en/4.1/ref/models/options/
    class Meta:
        # Blogs typically order by latest published...
        ordering = ['-publish']

        indexes = [
            models.Index(fields=['-publish'])
        ]


    def __str__(self):
        return self.title