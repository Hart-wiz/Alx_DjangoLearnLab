from django.db import models

# Create your models here.
from django.db import models

class Author(models.Model):
    # """
    # Author model
    # ------------
    # Purpose:
    #     Represents a single author. An Author can be linked to many Books
    #     via the one-to-many relationship defined on Book.author.

    # Fields:
    #     name (CharField): The author's display name.
    # """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    # """
    # Book model
    # ----------
    # Purpose:
    #     Represents a single book that belongs to exactly one Author.

    # Fields:
    #     title (CharField): Title of the book.
    #     publication_year (IntegerField): Year the book was published.
    #     author (ForeignKey -> Author): One-to-many relationship. Each Book
    #         references a single Author. We use related_name='books' to make
    #         reverse access (author.books) explicit and readable.
    # """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books"  # enables author.books.all()
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
