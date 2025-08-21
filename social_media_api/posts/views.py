from django.shortcuts import render

# Create your views here.
from django.db.models import Prefetch
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Post, Comment
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
from .pagination import DefaultPagination


class PostViewSet(viewsets.ModelViewSet):
    """
    /posts/ CRUD
    - List/search/order/paginate posts
    - Retrieve includes embedded comments
    - Extra nested route: /posts/{id}/comments (GET, POST)
    """
    queryset = Post.objects.select_related("author").prefetch_related(
        Prefetch("comments", queryset=Comment.objects.select_related("author"))
    )
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "content", "author__username"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
    pagination_class = DefaultPagination

    def get_serializer_class(self):
        # Return comments inline on detail
        if self.action == "retrieve":
            return PostDetailSerializer
        return PostSerializer

    def perform_create(self, serializer):
        # author set in serializer via request context; this is just explicit
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["get", "post"], url_path="comments")
    def comments(self, request, pk=None):
        """
        GET  /posts/{id}/comments   -> list comments for a post (paginated)
        POST /posts/{id}/comments   -> create comment for a post
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
    /comments/ CRUD
    - You can also create via nested /posts/{id}/comments (preferred).
    - Filter by ?post=<id>
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["created_at"]

    def get_queryset(self):
        qs = Comment.objects.select_related("author", "post")
        post_id = self.request.query_params.get("post")
        if post_id:
            qs = qs.filter(post_id=post_id)
        return qs

    def perform_create(self, serializer):
        # accept post from payload; serializer validates/attaches author
        serializer.save(author=self.request.user)
