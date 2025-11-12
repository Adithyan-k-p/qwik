from django.urls import path
from .views import (
    PostListCreateAPIView, PostDetailAPIView, PostLikeToggleAPIView,
    PostConvertAPIView, PostCommentsAPIView, CommentListCreateAPIView,
    CommentDetailAPIView
)

urlpatterns = [
    # Posts
    path('posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
    path('posts/<int:pk>/like/', PostLikeToggleAPIView.as_view(), name='post-like-toggle'),
    path('posts/<int:pk>/convert/', PostConvertAPIView.as_view(), name='post-convert'),
    path('posts/<int:pk>/comments/', PostCommentsAPIView.as_view(), name='post-comments'),

    # Comments
    path('comments/', CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetailAPIView.as_view(), name='comment-detail'),

]