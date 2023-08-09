from django import template
from ..models import Post

register: template.Library = template.Library()

@register.simple_tag
def total_posts() -> int:
    return Post.published.count()