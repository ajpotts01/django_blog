from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Third-party, non-Django
from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    # Another pattern for establishing enumeration-style choices
    # https://docs.djangoproject.com/en/4.1/ref/models/fields/#enumeration-types
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT
    )

    objects: models.Manager = models.Manager()
    published: PublishedManager = PublishedManager()
    tags: TaggableManager = TaggableManager()

    # Django pattern: nested class for defining metadata
    # https://docs.djangoproject.com/en/4.1/topics/db/models/#meta-options
    # https://docs.djangoproject.com/en/4.1/ref/models/options/
    class Meta:
        # Blogs typically order by latest published...
        ordering = ["-publish"]

        indexes = [models.Index(fields=["-publish"])]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            viewname="blog:post_detail",
            args=[self.publish.year, self.publish.month, self.publish.day, self.slug],
        )


class Comment(models.Model):
    post: models.ForeignKey = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )

    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created"]
        indexes = [models.Index(fields=["created"])]

    def __str__(self) -> str:
        return f"Comment by {self.name} on {self.post}"
