# Create your views here.
# relationship_app/views.py

from django.shortcuts import render, get_object_or_404
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView

# ✅ Function-Based View: list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# ✅ Class-Based View: details of a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'  # So you can access it in the template
