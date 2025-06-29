from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, TokenError

from .models import User
from Temp.validators import letter_validator, number_validator, special_char_validator


class InputRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = [
            "username",
            "name",
            "password",
            "confirm_password",
            "is_active",
            "is_admin",
            "is_superuser",
            "is_client_user",
        ]

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("This username already exists")
        return username

    def validate(self, data):
        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError("Confirm password is not equal to password")
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(
            username=validated_data.get("username"),
            password=validated_data.get("password"),
            name=validated_data.get("name"),
            is_active=validated_data.get("is_active", False),
            is_admin=validated_data.get("is_admin", False),
            is_client_user=validated_data.get("is_client_user", False),
        )
        return user


class OutPutRegisterSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField("get_token")

    class Meta:
        model = User
        fields = ("id", "username", "token", "created_at", "updated_at")

    def get_token(self, user):
        data = dict()
        token_class = RefreshToken

        refresh = token_class.for_user(user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=150)