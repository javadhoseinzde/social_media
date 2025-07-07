from django.urls import path

from .models import Profile
from .views import ProfileApi, ProfileDetailApi, FollowListApi, FollowApi

urlpatterns = [
    path("profile-list/", ProfileApi.as_view(), name="profile-list"),
    path("create-profile/", ProfileApi.as_view(), name="create-profile"),
    path("detail-profile/<int:id>/", ProfileDetailApi.as_view(), name="detail-create"),

    path("follower-list/", FollowListApi.as_view(),name="follower-list"),
    path("create-follower/", FollowApi.as_view(),name="create-follower"),

]