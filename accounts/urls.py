from django.urls import path

from accounts.views import *

urlpatterns = [
    path("register/", RegisterApi.as_view(), name="register"),

]

