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