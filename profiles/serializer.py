from rest_framework import serializers
from .models import Profile
from Temp.validators import *
from django.core.validators import MinLengthValidator

class ProfileSrializer(serializers.ModelSerializer):

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

    class Meta:
        model = Profile
        fields = [
            "user",
            "phone_number",
            "email",
            "picture",
            "bio",
            "link",
            "gender"
        ]
        read_only_fields = ['user']  # ✅ مهم برای جلوگیری از خطای required

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)