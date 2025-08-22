from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from notifications.models import Notification


# -------------------------
# Post ViewSet
# -------------------------
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# -------------------------
# Comment ViewSet
# -------------------------
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# -------------------------
# Feed View
# -------------------------
class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.values_list("following", flat=True)
        return Post.objects.filter(author__in=following_users).order_by("-created_at")


# -------------------------
# Like Post View
# -------------------------
class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # Find the post or return 404
        post = get_object_or_404(Post, pk=pk)

        # Create a Like object if not already liked
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if created:
            # Send notification only if a new like is created
            if post.author != request.user:  # prevent self-notification
                Notification.objects.create(
                    recipient=post.author,
                    actor=request.user,
                    verb="liked",
                    target=post,
                )
            return Response({"message": "Post liked."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "You already liked this post."}, status=status.HTTP_200_OK)


# -------------------------
# Unlike Post View
# -------------------------
class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response({"message": "Post unliked."}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({"message": "You haven't liked this post."}, status=status.HTTP_400_BAD_REQUEST)
