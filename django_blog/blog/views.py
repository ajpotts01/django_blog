from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request: HttpRequest) -> HttpResponse:
    posts: list[Post] = Post.published.all()

    return render(
        request=request, template_name="blog/post/list.html", context={"posts": posts}
    )


def post_detail(
    request: HttpRequest, year: int, month: int, day: int, post: str
) -> HttpResponse:
    post = get_object_or_404(
        klass=Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    return render(
        request=request, template_name="blog/post/detail.html", context={"post": post}
    )
