from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['user', 'is_active', 'converted_at', 'created_at', 'updated_at']

    def validate(self, data):
        post_type = data.get('post_type')
        expires_at = data.get('expires_at')

        if post_type == 'temporary' and not expires_at:
            raise serializers.ValidationError("Temporary posts must have an expiry time.")
        return data
