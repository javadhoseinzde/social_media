from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager as BUM
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class BaseUserManager(BUM):
    def create_user(
        self, username, is_active=True, is_admin=False, password=None
    ):
        if not username:
            raise ValueError("Users must have a Username")

        user = self.model(
            username=username,
            is_active=is_active,
            is_admin=is_admin,
        )

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(
            username=username,
            password=password,
        )

        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True

        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(unique=True, blank=True, null=True, max_length=11)
    email = models.EmailField(unique=True, blank=True, null=True)
    picture = models.ImageField(null=True, blank=True, upload_to="account/avatar")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_client_user = models.BooleanField(default=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BaseUserManager()

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username

    class Meta:
        db_table = "User"
