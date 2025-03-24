import uuid
import re
from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import ValidationError


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)

    def clean_username(self):
        self.username = self.username.lower()

        if len(self.username) > 30:
            raise ValidationError("Username cannot exceed 30 characters.")

        if not re.match(r'^[a-z0-9_]+$', self.username):
            raise ValidationError("Username can only contain lowercase Latin letters, numbers, and underscores.")

    def save(self, *args, **kwargs):
        self.clean_username()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", default='avatars/default_avatar.jpg')
    bio = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
