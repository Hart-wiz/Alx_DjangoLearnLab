from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from notifications.utils import create_notification


# Post CRUD
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.all().order_by("-created_at")

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        return post


# Comment CRUD
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs.get("post_pk"))

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        create_notification(
            sender=self.request.user,
            recipient=comment.post.author,
            verb="commented on your post",
            target=comment.post,
        )
        return comment


# Like a Post
class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.likes.add(request.user)
        create_notification(
            sender=request.user,
            recipient=post.author,
            verb="liked your post",
            target=post,
        )
        return Response({"detail": "Post liked."}, status=status.HTTP_200_OK)


# Unlike a Post
class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.likes.remove(request.user)
        return Response({"detail": "Post unliked."}, status=status.HTTP_200_OK)


# Feed (posts from followed users)
class FeedView(generics.GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        following_users = user.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by("-created_at")
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
