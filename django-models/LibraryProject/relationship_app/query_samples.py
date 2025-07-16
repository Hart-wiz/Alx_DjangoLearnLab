import os
import sys
import django

# Add the parent directory to Python path so it can find 'LibraryProject'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now Django can find the settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")

django.setup()


from relationship_app.models import *

# ✅ Create Author
author1 = Author.objects.create(name="Chinua Achebe")

# ✅ Create Books
book1 = Book.objects.create(title="Things Fall Apart", author=author1)
book2 = Book.objects.create(title="No Longer at Ease", author=author1)

# ✅ Create Library and add books
library1 = Library.objects.create(name="Central Library")
library1.books.add(book1, book2)

# ✅ Create Librarian
librarian1 = Librarian.objects.create(name="Mr. Obi", library=library1)

# =======================
# 🔎 Sample Queries
# =======================

# 1. All books by a specific author
print("Books by Chinua Achebe:")
for book in Book.objects.filter(author__name="Chinua Achebe"):
    print(f"- {book.title}")

# 2. List all books in a library
print(f"\nBooks in {library1.name}:")
for book in library1.books.all():
    print(f"- {book.title}")

# 3. Retrieve the librarian for a library
print(f"\nLibrarian for {library1.name}: {library1.librarian.name}")
