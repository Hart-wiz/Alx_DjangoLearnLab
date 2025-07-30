# LibraryProject/relationship_app/query_samples.py

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')  # Make sure this matches your project
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Optional: Clean up for repeated runs
Author.objects.all().delete()
Book.objects.all().delete()
Library.objects.all().delete()
Librarian.objects.all().delete()

# Sample data creation
author1 = Author.objects.create(name="Chinua Achebe")
author2 = Author.objects.create(name="Wole Soyinka")

book1 = Book.objects.create(title="Things Fall Apart", author=author1)
book2 = Book.objects.create(title="Arrow of God", author=author1)
book3 = Book.objects.create(title="The Lion and the Jewel", author=author2)

library1 = Library.objects.create(name="Central Library")
library1.books.set([book1, book2, book3])

librarian1 = Librarian.objects.create(name="Mrs. Grace", library=library1)

# ----------- Required Queries -----------

# ✅ 1. Get all books by a specific author
author_name = "Chinua Achebe"
try:
    author = Author.objects.get(name=author_name)
    books_by_author = Book.objects.filter(author=author)
    print(f"\n📚 Books by {author_name}:")
    for book in books_by_author:
        print(f"- {book.title}")
except Author.DoesNotExist:
    print(f"❌ Author '{author_name}' not found.")

# ✅ 2. List all books in a library using .get()
library_name = "Central Library"
try:
    library = Library.objects.get(name=library_name)
    print(f"\n🏛️ Books in {library_name}:")
    for book in library.books.all():
        print(f"- {book.title}")
except Library.DoesNotExist:
    print(f"❌ Library '{library_name}' not found.")

# ✅ 3. Retrieve librarian using Librarian.objects.get(library=...)
try:
    library = Library.objects.get(name=library_name)
    librarian = Librarian.objects.get(library=library)
    print(f"\n👩‍🏫 Librarian for {library_name}: {librarian.name}")
except (Library.DoesNotExist, Librarian.DoesNotExist):
    print(f"❌ Librarian for '{library_name}' not found.")
