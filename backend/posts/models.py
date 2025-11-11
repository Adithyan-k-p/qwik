from django.db import models
from users.models import User
from django.utils import timezone

class Post(models.Model):
    POST_TYPE_CHOICES = (
        ('temporary', 'Temporary'),
        ('permanent', 'Permanent'),
    )

    MEDIA_TYPE_CHOICES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField(blank=True)
    media_url = models.URLField(blank=True, null=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, blank=True)
    post_type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES, default='permanent')
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    converted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def check_expiry(self):
        if self.post_type == 'temporary' and self.expires_at and timezone.now() > self.expires_at:
            self.is_active = False
            self.save()

    def __str__(self):
        return f"{self.user.username} - {self.post_type} post"
