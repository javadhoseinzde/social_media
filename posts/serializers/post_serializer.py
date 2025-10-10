from rest_framework import serializers
from posts.models.post import Post

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        models = Post
        exclude = [
            "created_at",
            "updated_at",
            "likes_count",
            "comments_count"
        ]