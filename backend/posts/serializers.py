from rest_framework import serializers
from .models import Post, Like, Comment
from users.serializers import UserSerializer  # Assuming you have one in users/serializers.py

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'text', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'user', 'caption', 'media_url', 'media_type', 'post_type',
            'is_active', 'expires_at', 'converted_at', 'created_at', 'updated_at',
            'likes_count', 'comments_count', 'has_liked'
        ]
        read_only_fields = ['id', 'user', 'is_active', 'created_at', 'updated_at', 'likes_count', 'comments_count', 'has_liked']

    def get_likes_count(self, obj):
        return obj.likes_received.count()

    def get_comments_count(self, obj):
        return obj.comments_received.count()

    def get_has_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes_received.filter(user=request.user).exists()
        return False

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)