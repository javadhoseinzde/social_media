from rest_framework import serializers
from posts.models.post import Post
from accounts.models import User

class PostSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    mentions = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=False
    )
    class Meta:
        model = Post
        fields = "__all__"

    def validate(self, attrs):
        caption = attrs.get('caption')
        image = attrs.get('image')

        if not caption and not image:
            raise serializers.ValidationError(
                {"non_field_error": "Post must contain at least a caption or an image."}
            )
        return attrs