from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager as BUM
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class BaseUserManager(BUM):
    def create_user(
        self, username, name, is_active=True, is_admin=False, is_client_user=True, password=None
    ):
        print(name)
        if not username:
            raise ValueError("Users must have a Username")

        user = self.model(
            username=username,
            is_active=is_active,
            is_admin=is_admin,
            is_client_user=is_client_user,
            name=name
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
        return str(self.username)

    class Meta:
        db_table = "profile"
