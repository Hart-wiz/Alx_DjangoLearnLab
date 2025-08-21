from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Post, Comment

User = get_user_model()


class UserBriefSerializer(serializers.ModelSerializer):
    """Public, minimal user info for embedding in Post/Comment responses."""
    # If your custom User has profile_picture, expose its URL safely.
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "avatar")

    def get_avatar(self, obj):
        pic = getattr(obj, "profile_picture", None)
        try:
            return pic.url if pic else None
        except Exception:
            return None


class PostSerializer(serializers.ModelSerializer):
    author = UserBriefSerializer(read_only=True)
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "title",
            "content",
            "created_at",
            "updated_at",
            "comments_count",
        )
        read_only_fields = ("id", "author", "created_at", "updated_at", "comments_count")

    # Attach the authenticated user as author
    def create(self, validated_data):
        request = self.context.get("request")
        if not request or not request.user or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication required.")
        validated_data["author"] = request.user
        return super().create(validated_data)

    # Light validation / normalization
    def validate_title(self, value: str):
        v = value.strip()
        if len(v) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters.")
        return v

    def validate_content(self, value: str):
        v = value.strip()
        if not v:
            raise serializers.ValidationError("Content cannot be empty.")
        return v


class CommentSerializer(serializers.ModelSerializer):
    author = UserBriefSerializer(read_only=True)
    # For writes: accept post as PK. For reads: expose post_id.
    post = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(), write_only=True, required=False
    )
    post_id = serializers.IntegerField(source="post.id", read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "post",        # write-only
            "post_id",     # read-only
            "author",
            "content",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "author", "post_id", "created_at", "updated_at")

    def create(self, validated_data):
        """
        Creates a comment and auto-sets:
        - author from request.user
        - post from either payload 'post' or the view's context (e.g., nested route)
        """
        request = self.context.get("request")
        if not request or not request.user or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication required.")

        # prefer post passed via payload; else accept from context (for nested routes /posts/<pk>/comments/)
        post = validated_data.pop("post", None) or self.context.get("post")
        if not post:
            raise serializers.ValidationError({"post": "Post is required."})

        validated_data["author"] = request.user
        validated_data["post"] = post
        return super().create(validated_data)

    def validate_content(self, value: str):
        v = value.strip()
        if not v:
            raise serializers.ValidationError("Comment content cannot be empty.")
        if len(v) > 2000:
            raise serializers.ValidationError("Comment is too long (max 2000 chars).")
        return v


class PostDetailSerializer(PostSerializer):
    """Post with embedded comments for detail endpoints."""
    comments = CommentSerializer(many=True, read_only=True)

    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ("comments",)
