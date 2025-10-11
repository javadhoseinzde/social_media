from django.urls import path

from .views.post_views import PostApi

urlpatterns = [
    path("post-list/", PostApi.as_view(), name="post-list"),
    path("create-post/", PostApi.as_view(), name="create-post"),
]