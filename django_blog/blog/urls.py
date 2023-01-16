from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path(route="", view=views.post_list, name="post_list"),
    path(route="<int:id>/", view=views.post_detail, name="post_detail"),
]
