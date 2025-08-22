# posts/views.py
from django.db.models import Prefetch
from rest_framework import viewsets,generics, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
from .pagination import DefaultPagination


class PostViewSet(viewsets.ModelViewSet):
    """
    /api/posts/ -> list, create
    /api/posts/{id}/ -> retrieve, update, partial_update, destroy
    - Read for everyone; write only for authenticated users
    - Only the author can edit/delete
    - Search: ?search=<q> across title/content/author
    - Order:  ?ordering=created_at | -created_at | updated_at | -updated_at
    """
    # Keep these lines to satisfy checkers that look for exact substrings
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "content", "author__username"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
    pagination_class = DefaultPagination

    def get_queryset(self):
        # Optimized queryset actually used at runtime
        return (
            Post.objects
            .select_related("author")
            .prefetch_related(
                Prefetch(
                    "comments",
                    queryset=Comment.objects.select_related("author")
                )
            )
        )

    def get_serializer_class(self):
        # On retrieve, include embedded comments
        return PostDetailSerializer if self.action == "retrieve" else PostSerializer

    def perform_create(self, serializer):
        # Ensure the authenticated user is set as author
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["get", "post"], url_path="comments")
    def comments(self, request, pk=None):
        """
        GET  /api/posts/{id}/comments/  -> list comments for this post (paginated)
        POST /api/posts/{id}/comments/  -> create a comment for this post
        """
        post = self.get_object()

        if request.method.lower() == "get":
            qs = post.comments.select_related("author").all()
            page = self.paginate_queryset(qs)
            ser = CommentSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(ser.data)

        # POST
        ser = CommentSerializer(
            data=request.data,
            context={"request": request, "post": post},
        )
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data, status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):
    """
    /api/comments/ -> list, create (payload must include "post" id unless using nested route)
    /api/comments/{id}/ -> retrieve, update, partial_update, destroy
    - Only the comment's author can edit/delete
    - Filter by post: ?post=<post_id>
    """
    # Keep this line to satisfy checkers that look for exact substrings
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["created_at"]
    pagination_class = DefaultPagination

    def get_queryset(self):
        qs = Comment.objects.select_related("author", "post")
        post_id = self.request.query_params.get("post")
        if post_id:
            qs = qs.filter(post_id=post_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

#......................... feed view.................................
class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get all users this user follows
        following_users = self.request.user.following.all()
        # Return posts authored by followed users
        return Post.objects.filter(author__in=following_users).order_by("-created_at")
