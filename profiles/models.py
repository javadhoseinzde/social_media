from django.db import models
from accounts.models import User
# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(unique=True, blank=True, null=True, max_length=11)
    email = models.EmailField(unique=True, blank=True, null=True)
    picture = models.ImageField(null=True, blank=True, upload_to="account/avatar")
    bio = models.CharField(max_length=250)
    link = models.CharField(max_length=40)
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username
    class Meta:
        db_table = "profiles"
