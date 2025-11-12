from django.db import models
from django.utils import timezone
from users.models import User  # Assuming User is in users app

class Post(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('text', 'Text'),
    ]
    POST_TYPE_CHOICES = [
        ('temporary', 'Temporary'),
        ('permanent', 'Permanent'),
    ]
    
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField(blank=True, null=True)
    media_url = models.URLField(blank=True, null=True)  # Firebase URL
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='text')
    post_type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES, default='temporary')
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    converted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.post_type == 'temporary' and not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(hours=24)
        super().save(*args, **kwargs)
        # Auto-deactivate if expired (call this in a Celery task for production, but simple check here)
        if self.expires_at and self.expires_at < timezone.now() and self.is_active:
            self.is_active = False
            super().save(update_fields=['is_active'])

    def __str__(self):
        return f"Post {self.id} by {self.user.username}"

class Like(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_given')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes_received')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        indexes = [models.Index(fields=['user', 'post'])]

    def __str__(self):
        return f"{self.user.username} liked {self.post.id}"

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_made')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments_received')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment {self.id} by {self.user.username} on Post {self.post.id}"