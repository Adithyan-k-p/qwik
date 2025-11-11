from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Post
from .serializers import PostSerializer
from django.utils import timezone


class PostCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        # 1. Instantiate serializer with incoming data
        serializer = PostSerializer(data=request.data)

        # 2. Validate data
        if serializer.is_valid():
            # 3. Save instance, manually setting the current user (perform_create logic)
            serializer.save(user=request.user)
            
            # 4. Return success response
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # 5. Return error response if validation fails
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class  PostListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        # 1. Replicate the get_queryset logic
        now = timezone.now()
        queryset = Post.objects.filter(
            is_active=True
        ).exclude(
            post_type='temporary',
            expires_at__lt=now
        ).order_by('-created_at')

        # 2. Instantiate serializer (must set many=True for a list/queryset)
        serializer = PostSerializer(queryset, many=True)
        
        # 3. Return serialized data
        return Response(serializer.data)

class PostDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        # 1. Try to find the post by ID and ensure it's active
        post = get_object_or_404(Post, id=post_id, is_active=True)

        # 2. Serialize the post object
        serializer = PostSerializer(post)

        # 3. Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, post_id):
        # 1. Try to find the post by ID
        post = get_object_or_404(Post, id=post_id)

        # 2. Check if the current user is the owner
        if post.user != request.user:
            return Response(
                {"detail": "You do not have permission to delete this post."},
                status=status.HTTP_403_FORBIDDEN
            )

        # 3. Delete the post
        post.delete()

        # 4. Return success response
        return Response(
            {"detail": "Post deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
