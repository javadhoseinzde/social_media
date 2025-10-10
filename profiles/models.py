from django.db import models
from accounts.models import User
# Create your models here.

class Profile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(unique=True, blank=True, null=True, max_length=11)
    email = models.EmailField(unique=True, blank=True, null=True)
    picture = models.ImageField(null=True, blank=True, upload_to="account/avatar")
    bio = models.CharField(max_length=250, blank=True)
    link = models.CharField(max_length=40, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = "profiles"


class Follower(models.Model):
    from_user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user} follows {self.to_user}"