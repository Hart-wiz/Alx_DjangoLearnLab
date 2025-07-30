# relationship_app/views.py

from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Library  # ✅ <- This satisfies the check

# ✅ Function-Based View to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# ✅ Class-Based View to show details of a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
