from django.db import models
from accounts.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    caption = models.TextField(max_length=2200, blank=True)
    image = models.ImageField(upload_to='posts/images/', blank=True, null=True)
    video = models.FileField(upload_to='posts/videos/', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)
    mentions = models.ManyToManyField(User, related_name='tagged_posts', blank=True)

    is_active = models.BooleanField(default=True) #publish
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}: {self.caption[:30]}"

    class Meta:
        ordering = ['-created_at']