from django.contrib import admin

from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display: list[str] = ["title", "slug", "author", "publish", "status"]
    list_filter: list[str] = ["status", "created", "publish", "author"]
    search_fields: list[str] = ["title", "body"]
    prepopulated_fields: dict = {
        "slug": ["title"]  # Why was this a tuple of 1 in the examples?
    }
    raw_id_fields: list[str] = ["author"]
    date_hierarchy: str = "publish"
    ordering: list[str] = ["status", "publish"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display: list[str] = ["name", "email", "post", "created", "active"]
    list_filter: list[str] = ["active", "created", "updated"]
    search_fields: list[str] = ["name", "email", "body"]
