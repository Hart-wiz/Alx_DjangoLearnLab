from datetime import date
from rest_framework import serializers
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    # """
    # BookSerializer
    # --------------
    # Purpose:
    #     Serializes Book instances. Includes a validation rule to ensure
    #     'publication_year' is not set in the future.

    # Notes:
    #     - ModelSerializer automatically maps model fields.
    #     - Custom validate_<field> method enforces a domain rule.
    # """
    class Meta:
        model = Book
        fields = ["id", "title", "publication_year", "author"]

    def validate_publication_year(self, value):
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                f"publication_year cannot be in the future (>{current_year})."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    # """
    # AuthorSerializer
    # ----------------
    # Purpose:
    #     Serializes Author instances along with the author's related books.

    # Relationship handling:
    #     - Uses the reverse relation 'books' (from Book.author related_name).
    #     - 'books' is nested using BookSerializer with many=True, read_only=True
    #       (read-only avoids write-time complexity for nested create/update;
    #       you can add custom create/update if you need writable nesting later).
    # """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ["id", "name", "books"]
