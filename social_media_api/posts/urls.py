from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView

# DRF router for posts & comments
router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")
router.register(r"comments", CommentViewSet, basename="comment")

# Router URLs + custom paths
urlpatterns = router.urls + [
    path("feed/", FeedView.as_view(), name="feed"),
]
