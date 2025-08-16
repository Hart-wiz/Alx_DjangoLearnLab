from django.shortcuts import render
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer
# Create your views here.



class BookListView(generics.ListAPIView):
    # """
    # GET /api/books/
    # Public, read-only list of all books with optional filters, search, and ordering.
    # """
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

    # Nice-to-have: filters & search
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["publication_year", "author"]  # /api/books/?publication_year=1958&author=1
    search_fields = ["title"]                           # /api/books/?search=things
    ordering_fields = ["publication_year", "title"]     # /api/books/?ordering=-publication_year
    ordering = ["-publication_year"]                    # default order


class BookDetailView(generics.RetrieveAPIView):
    # """
    # GET /api/books/<pk>/
    # Public, read-only detail for a single book.
    # """
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    """
    POST /api/books/create/
    Authenticated-only. Validates via BookSerializer (incl. future-year rule).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Hook for extra logic (e.g., attach owner/user if your model had it).
        # Validation already handled in the serializer.
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH /api/books/<pk>/update/
    Authenticated-only. Supports full (PUT) and partial (PATCH) updates.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        # Hook for extra logic on update if needed.
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /api/books/<pk>/delete/
    Authenticated-only. Returns 204 No Content on success.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
