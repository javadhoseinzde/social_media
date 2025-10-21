from django.urls import path

from .views.post_views import PostApi, PostDetailApi

urlpatterns = [
    path("posts", PostApi.as_view(), name="posts"),
    path("post-detail/<int:id>/", PostDetailApi.as_view(), name="post-detail")
]