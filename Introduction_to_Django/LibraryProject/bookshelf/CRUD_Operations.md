# CRUD Operations for Book Model in Django

🔹 Create

from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(book)

Output:
1984 by George Orwell (1949)

🔹 Retrieve

book = Book.objects.get(title="1984")
print(book.title, book.author, book.publication_year)

Output:
1984 George Orwell 1949

🔹 Update

book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(book.title)

Output:
Nineteen Eighty-Four

🔹 Delete

book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
print(Book.objects.all())

Output:
<QuerySet []>

✅ Summary
Book model was successfully defined with title, author, and publication_year.

CRUD operations were executed using Django ORM.

All actions were documented with expected outputs.
