from rest_framework import serializers
from .models import Profile, Follower
from Temp.validators import *
from django.core.validators import MinLengthValidator
from accounts.models import User
class ProfileSerializer(serializers.ModelSerializer):

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
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ["to_user"]

class ToUserSerializer(serializers.Serializer):
    user = serializers.CharField()
    picture = serializers.ImageField()

class FollowerSerializer(serializers.ModelSerializer):
    to_user = serializers.SerializerMethodField()

    class Meta:
        model = Follower
        fields = ["id","to_user"]

    def get_to_user(self, obj):
        try:
            profile = Profile.objects.get(user=obj.to_user)
            result = ProfileSerializer(profile, context=self.context).data
            return {
                "user": obj.to_user.username,
                "picture": result.get("picture")
            }
        except Profile.DoesNotExist:
            return None