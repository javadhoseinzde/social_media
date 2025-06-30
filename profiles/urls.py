from django.urls import path
from .views import ProfileApi, ProfileDetailApi

urlpatterns = [
    path("profile-list/", ProfileApi.as_view()),
    path("create-profile/", ProfileApi.as_view()),
    path("detail-profile/<int:id>/", ProfileDetailApi.as_view())


]