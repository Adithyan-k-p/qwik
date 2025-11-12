from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Follow

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Validates password match and strength.
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT serializer - adds user details to token response.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        token['is_verified'] = user.is_verified
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Add custom fields to response
        data.update({
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'bio': self.user.bio,
            'profile_image': self.user.profile_image,
            'is_verified': self.user.is_verified,
            'role': self.user.role,
        })
        return data

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user profiles and nested use (e.g., in posts).
    Excludes sensitive fields; read-only for IDs/timestamps.
    """
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'bio', 'profile_image',
            'is_verified', 'role', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'email', 'role', 'is_active', 'created_at', 'updated_at']

class FollowSerializer(serializers.ModelSerializer):
    """
    Serializer for follow relationships.
    """
    follower = UserSerializer(read_only=True)
    following = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']
        read_only_fields = ['id', 'created_at', 'follower']

    def create(self, validated_data):
        validated_data['follower'] = self.context['request'].user
        return super().create(validated_data)