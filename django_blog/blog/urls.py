from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path(route="", view=views.post_list, name="post_list"),
    path(route="tag/<slug:tag_slug>/", view=views.post_list, name="post_list_by_tag"),
    # path('', view=views.PostListView.as_view(), name='post_list'),
    path(
        route="<int:year>/<int:month>/<int:day>/<slug:post>/",
        view=views.post_detail,
        name="post_detail",
    ),
    path(route="<int:post_id>/share/", view=views.post_share, name="post_share"),
    path(route="<int:post_id>/comment/", view=views.post_comment, name="post_comment"),
]
