# Django imports
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView

# Project imports
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm


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
    post: Post = get_object_or_404(
        klass=Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    # Is the type correct?
    comments: list[Comment] = post.comments.filter(active=True)
    form: CommentForm = CommentForm()

    return render(
        request=request,
        template_name="blog/post/detail.html",
        context={"post": post, "comments": comments, "form": form},
    )


def post_share(request: HttpRequest, post_id: int) -> HttpResponse:
    post: Post = get_object_or_404(klass=Post, id=post_id, status=Post.Status.PUBLISHED)
    sent: bool = False

    if request.method == "POST":
        form: EmailPostForm = EmailPostForm(request.POST)

        if form.is_valid():
            cd: dict = form.cleaned_data

            # Send e-mail
            post_url: str = request.build_absolute_uri(post.get_absolute_url())
            subject: str = f"{cd['name']} recommends you read {post.title}"
            message: str = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )

            send_mail(subject, message, "test@gmail.com", [cd["to"]])
            sent = True
    else:
        form: EmailPostForm = EmailPostForm()

    return render(
        request=request,
        template_name="blog/post/share.html",
        context={"post": post, "form": form, "sent": sent},
    )


@require_POST
def post_comment(request: HttpRequest, post_id: int) -> HttpResponse:
    post: Post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)

    comment: Comment = None
    form: CommentForm = CommentForm(data=request.POST)

    if form.is_valid():
        # form.save creates objects without committing
        comment = form.save(commit=False)
        comment.post = post

        # This actually commits the new comment to the database
        comment.save()

    return render(
        request=request,
        template_name="blog/post/comment.html",
        context={"post": post, "form": form, "comment": comment},
    )
