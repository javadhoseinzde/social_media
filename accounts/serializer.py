from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, TokenError

from .models import User
from Temp.validators import letter_validator, number_validator, special_char_validator


class InputRegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False)
    phone_number = serializers.CharField(
        validators=[
            number_validator,
            letter_validator,
            special_char_validator,
            MinLengthValidator(limit_value=11),
        ],
        max_length=11,
        required=False,
    )
    email = serializers.EmailField(required=False)
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    confirm_password = serializers.CharField(max_length=255)
    is_admin = serializers.BooleanField(default=False)
    is_superuser = serializers.BooleanField(default=False)

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("This username is exist")
        return username

    def validate(self, data):
        if not data.get("password") or not data.get("confirm_password"):
            raise serializers.ValidationError(
                "Please fill password and confirm password"
            )

        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError(
                "confirm password is not equal to password"
            )
        return data


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