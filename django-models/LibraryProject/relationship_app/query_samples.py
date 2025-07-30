# relationship_app/query_samples.py

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')  # Use your actual project name
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Clean up old data (optional for repeated runs)
Author.objects.all().delete()
Book.objects.all().delete()
Library.objects.all().delete()
Librarian.objects.all().delete()

# Create sample data
author1 = Author.objects.create(name="Chinua Achebe")
author2 = Author.objects.create(name="Wole Soyinka")

book1 = Book.objects.create(title="Things Fall Apart", author=author1)
book2 = Book.objects.create(title="Arrow of God", author=author1)
book3 = Book.objects.create(title="The Lion and the Jewel", author=author2)

library1 = Library.objects.create(name="Central Library")
library1.books.set([book1, book2, book3])

librarian1 = Librarian.objects.create(name="Mrs. Grace", library=library1)

# ----------- Required Queries -----------

# 1. Query all books by a specific author
print("📚 Books by Chinua Achebe:")
books_by_achebe = Book.objects.filter(author__name="Chinua Achebe")
for book in books_by_achebe:
    print(f"- {book.title}")

# 2. List all books in a specific library using get()
library_name = "Central Library"
try:
    lib = Library.objects.get(name=library_name)
    print(f"\n📖 Books in {library_name}:")
    for book in lib.books.all():
        print(f"- {book.title}")
except Library.DoesNotExist:
    print(f"Library named '{library_name}' not found.")

# 3. Retrieve the librarian for a specific library
try:
    lib = Library.objects.get(name=library_name)
    librarian = lib.librarian  # Using the reverse relation from OneToOneField
    print(f"\n👩‍🏫 Librarian for {library_name}: {librarian.name}")
except (Library.DoesNotExist, Librarian.DoesNotExist):
    print(f"Librarian for '{library_name}' not found.")
