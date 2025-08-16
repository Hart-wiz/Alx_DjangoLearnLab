from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated  # <- required
from django_filters.rest_framework import DjangoFilterBackend

from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    """
    GET /api/books/
    Public list endpoint with filtering, searching, and ordering.
    """
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # unauthenticated can GET

    # Enable filter/search/order on this endpoint
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # 1) Filtering by equality (?title=..., ?author=1, ?publication_year=1958)
    filterset_fields = ["title", "author", "publication_year"]

    # 2) Searching (partial, case-insensitive); includes author name via FK
    #    Examples: ?search=fall  or  ?search=achebe
    search_fields = ["title", "author__name"]

    # 3) Ordering (sorting)
    #    Examples: ?ordering=title  or  ?ordering=-publication_year
    ordering_fields = ["title", "publication_year"]
    ordering = ["-publication_year"]  # default sort


class BookDetailView(generics.RetrieveAPIView):
    """
    GET /api/books/<pk>/
    Public detail endpoint for a single book.
    """
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # unauthenticated can GET


class BookCreateView(generics.CreateAPIView):
    """
    POST /api/books/create/
    Authenticated-only create endpoint.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # writes require auth

    def perform_create(self, serializer):
        # Hook for extra logic (e.g., set owner) if needed
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH /api/books/update/<pk>/
    Authenticated-only update endpoint.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # writes require auth

    def perform_update(self, serializer):
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /api/books/delete/<pk>/
    Authenticated-only delete endpoint.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # writes require auth
