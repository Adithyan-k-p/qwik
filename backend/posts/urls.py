from django.urls import path
from .views import PostCreateView, PostDetailView, PostListView

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('<int:post_id>/', PostDetailView.as_view(), name='post-detail'),
]
