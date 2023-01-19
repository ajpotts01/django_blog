from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post

# class PostListView(ListView):
#     """
#     Alternative post list view - to demonstrate class-based views over function-based views
#     """
#     queryset: list[Post] = Post.published.all()
#     context_object_name: str = 'posts'
#     paginate_by: int = 3
#     template_name: str = 'blog/post/list.html'

def post_list(request: HttpRequest) -> HttpResponse:
    posts: list[Post] = Post.published.all()

    paginator: Paginator = Paginator(object_list=posts, per_page=3)
    # Can't explicitly state param __key: get is a dictionary method
    page_number: str = request.GET.get("page", default=1)

    try:
        posts = paginator.page(number=page_number)
    except EmptyPage:
        posts = paginator.page(number=paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(number=1)

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
