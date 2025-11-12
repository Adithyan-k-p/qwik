from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    """
    Custom User model for Qwik - extends Django's AbstractUser.
    Fields match your schema: username, email (unique/login), password (hashed),
    profile_image (Firebase URL), bio, role (user/admin), is_active, is_verified, timestamps.
    """
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    profile_image = models.URLField(blank=True, null=True, help_text="Firebase URL for profile photo")
    bio = models.TextField(blank=True, null=True, max_length=500, help_text="User bio")
    role = models.CharField(
        max_length=10,
        choices=[('user', 'User'), ('admin', 'Admin')],
        default='user'
    )
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False, help_text="Verified badge")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'  # Login with email
    REQUIRED_FIELDS = ['username']

    class Meta:
        indexes = [models.Index(fields=['email', 'username'])]

    def __str__(self):
        return self.username

class Follow(models.Model):
    """
    Tracks follows for social graph (e.g., personal feed in posts).
    """
    id = models.AutoField(primary_key=True)
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        indexes = [models.Index(fields=['follower', 'following'])]

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"