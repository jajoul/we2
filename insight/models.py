from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Channel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_channels')
    name = models.CharField(max_length=100)
    about = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/channels/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
