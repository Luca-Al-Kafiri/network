from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.CharField(max_length=64)
    post = models.TextField()
    timestamp = models.DateTimeField(default=datetime.now, blank=True)
    like = models.ManyToManyField(User, related_name='like', blank=True, null=True)
    liked = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user}'s post {self.id}"


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")

    def __str__(self):
        return f'{self.user} follows {self.following}'