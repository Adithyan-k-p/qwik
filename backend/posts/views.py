from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count
from .models import Post, Like, Comment
from .serializers import PostSerializer, CommentSerializer
import uuid
from qwik_backend.settings import supabase as client




class PostListCreateAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Build queryset similar to ViewSet
        posts = Post.objects.filter(is_active=True).select_related('user').annotate(
            likes_count=Count('likes_received'),
            comments_count=Count('comments_received')
        ).order_by('-created_at')
        user = request.user

        # Feed logic
        if 'feed' in request.query_params:
            followed_users = user.following.all().values_list('following_id', flat=True)  # Assumes Follow model in users
            posts = posts.filter(user_id__in=[user.id] + list(followed_users))

        # Trending
        elif 'trending' in request.query_params:
            posts = posts.order_by('-likes_count', '-comments_count')

        # Search
        if search := request.query_params.get('search'):
            posts = posts.filter(caption__icontains=search)

        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        # Handle media upload if file is present
        if 'media' in request.FILES:
            file = request.FILES['media']
            file_extension = file.name.split('.')[-1]
            file_name = f"{uuid.uuid4()}.{file_extension}"
            if client is None:
                return Response({'error': 'Supabase service unavailable (Configuration check needed)'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            try:
                with file.open('rb') as f:
                    res = client.storage.from_('qwips').upload(
                        file_name,
                        f.read(),
                        file_options={'content-type': file.content_type, 'upsert': 'true'}
                    )
                if hasattr(res, 'error') and res.error:
                    return Response({'error': f"Upload failed (Supabase API Error): {res.error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                media_url = client.storage.from_('qwips').get_public_url(file_name)
                data['media_url'] = media_url
            except Exception as e:
                return Response({'error': f'Supabase Upload Failed (API Call Error): {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = PostSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            post = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetailAPIView(APIView):
    parser_classes = [JSONParser]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        post = get_object_or_404(Post.objects.filter(is_active=True).select_related('user'), pk=pk)
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):  # Update (e.g., edit caption)
        post = get_object_or_404(Post.objects.filter(is_active=True, user=request.user), pk=pk)
        serializer = PostSerializer(post, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = get_object_or_404(Post.objects.filter(user=request.user), pk=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PostLikeToggleAPIView(APIView):
    parser_classes = [JSONParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post.objects.filter(is_active=True), pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        likes_count = post.likes_received.count()
        return Response({'liked': liked, 'likes_count': likes_count}, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)

class PostConvertAPIView(APIView):
    parser_classes = [JSONParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post.objects.filter(is_active=True), pk=pk)
        if post.user != request.user or post.post_type != 'temporary':
            return Response({'error': 'Unauthorized or not temporary'}, status=status.HTTP_403_FORBIDDEN)
        post.post_type = 'permanent'
        post.expires_at = None
        post.converted_at = timezone.now()
        post.save()
        # TODO: Log activity
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)

class PostCommentsAPIView(APIView):
    parser_classes = [JSONParser]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        post = get_object_or_404(Post.objects.filter(is_active=True), pk=pk)
        comments = post.comments_received.select_related('user').order_by('-created_at')
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

class CommentListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        post_id = request.query_params.get('post')
        if not post_id:
            return Response({'error': 'Post ID required'}, status=status.HTTP_400_BAD_REQUEST)
        comments = Comment.objects.filter(post_id=post_id).select_related('user', 'post').order_by('-created_at')
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            comment = serializer.save(user=request.user)
            # TODO: Trigger notification to post owner
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetailAPIView(APIView):
    parser_classes = [JSONParser]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        comment = get_object_or_404(Comment.objects.select_related('user', 'post'), pk=pk)
        serializer = CommentSerializer(comment, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        comment = get_object_or_404(Comment.objects.filter(user=request.user), pk=pk)
        serializer = CommentSerializer(comment, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = get_object_or_404(Comment.objects.filter(user=request.user), pk=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
# class UploadMediaAPIView(APIView):
#     parser_classes = [MultiPartParser, FormParser, JSONParser]
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         if 'media' not in request.FILES:
#             return Response({'error': 'No media file provided'}, status=status.HTTP_400_BAD_REQUEST)

#         file = request.FILES['media']
#         file_extension = file.name.split('.')[-1]
#         file_name = f"{uuid.uuid4()}.{file_extension}"  # No need for 'qwips/' prefix if bucket is 'qwips'

#         # Upload to Supabase (using global client)
#         with file.open('rb') as f:
#             res = settings.supabase.storage.from_('qwips').upload(file_name, f.read(), file_options={
#                 'content-type': file.content_type,
#                 'upsert': True  # Overwrite if exists
#             })

#         if not res.data:  # Success check (res.status_code not always set)
#             return Response({'error': 'Upload failed - check policies'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         # Get public URL
#         public_url = settings.supabase.storage.from_('qwips').get_public_url(file_name)
#         return Response({'media_url': public_url}, status=status.HTTP_201_CREATED)