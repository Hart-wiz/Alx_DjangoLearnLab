"""
Unit tests for Book API endpoints (Django REST Framework).

Covers:
- CRUD operations and permissions
- Filtering (?title=, ?author=, ?publication_year=)
- Searching (?search= across title, author__name)
- Ordering (?ordering=title, ?ordering=-publication_year)

Run:
    python manage.py test api -v 2
"""

from datetime import date

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Author, Book


class BookAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Users
        User = get_user_model()
        cls.user = User.objects.create_user(username="tester", password="pass1234")

        # Authors
        cls.author1 = Author.objects.create(name="Chinua Achebe")
        cls.author2 = Author.objects.create(name="Wole Soyinka")

        # Books
        cls.book1 = Book.objects.create(
            title="Things Fall Apart",
            publication_year=1958,
            author=cls.author1,
        )
        cls.book2 = Book.objects.create(
            title="No Longer at Ease",
            publication_year=1960,
            author=cls.author1,
        )
        cls.book3 = Book.objects.create(
            title="Ake",
            publication_year=1981,
            author=cls.author2,
        )

    # ----- URL helpers -----
    def list_url(self):
        return reverse("book-list")

    def create_url(self):
        return reverse("book-create")

    def detail_url(self, pk: int):
        return reverse("book-detail", args=[pk])

    def update_url(self, pk: int):
        # matches api/urls.py path("books/update/<int:pk>/", ...)
        return reverse("book-update", args=[pk])

    def delete_url(self, pk: int):
        # matches api/urls.py path("books/delete/<int:pk>/", ...)
        return reverse("book-delete", args=[pk])

    # ---------- READ-ONLY (AllowAny) ----------
    def test_list_books_as_anonymous_ok(self):
        response = self.client.get(self.list_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # uses response.data

    def test_retrieve_book_as_anonymous_ok(self):
        response = self.client.get(self.detail_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Things Fall Apart")
        self.assertEqual(response.data["author"], self.author1.id)

    # ---------- CREATE (IsAuthenticated) ----------
    def test_create_book_unauthenticated_is_unauthorized(self):
        payload = {
            "title": "Arrow of God",
            "publication_year": 1964,
            "author": self.author1.id,
        }
        response = self.client.post(self.create_url(), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_authenticated_ok(self):
        self.client.force_login(self.user)
        payload = {
            "title": "Arrow of God",
            "publication_year": 1964,
            "author": self.author1.id,
        }
        response = self.client.post(self.create_url(), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Arrow of God")
        self.assertEqual(response.data["publication_year"], 1964)
        self.assertEqual(response.data["author"], self.author1.id)
        self.assertTrue(Book.objects.filter(title="Arrow of God").exists())

    def test_create_book_future_year_rejected(self):
        self.client.force_login(self.user)
        future_year = date.today().year + 1
        payload = {
            "title": "From the Future",
            "publication_year": future_year,
            "author": self.author1.id,
        }
        response = self.client.post(self.create_url(), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("publication_year", response.data)  # uses response.data

    # ---------- UPDATE (IsAuthenticated) ----------
    def test_update_book_unauthenticated_is_unauthorized(self):
        payload = {
            "title": "Things Fall Apart (Updated)",
            "publication_year": 1958,
            "author": self.author1.id,
        }
        response = self.client.put(self.update_url(self.book1.id), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_authenticated_ok(self):
        self.client.force_login(self.user)
        payload = {
            "title": "Things Fall Apart (Updated)",
            "publication_year": 1958,
            "author": self.author1.id,
        }
        response = self.client.put(self.update_url(self.book1.id), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Things Fall Apart (Updated)")

    def test_partial_update_book_authenticated_ok(self):
        self.client.force_login(self.user)
        payload = {"title": "Things Fall Apart (2nd ed.)"}
        response = self.client.patch(self.update_url(self.book1.id), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Things Fall Apart (2nd ed.)")

    # ---------- DELETE (IsAuthenticated) ----------
    def test_delete_book_unauthenticated_is_unauthorized(self):
        response = self.client.delete(self.delete_url(self.book2.id))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_authenticated_ok(self):
        self.client.force_login(self.user)
        response = self.client.delete(self.delete_url(self.book2.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book2.id).exists())

    # ---------- FILTERING ----------
    def test_filter_by_author(self):
        response = self.client.get(f"{self.list_url()}?author={self.author1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = {b["title"] for b in response.data}
        self.assertSetEqual(titles, {"Things Fall Apart", "No Longer at Ease"})

    def test_filter_by_publication_year(self):
        response = self.client.get(f"{self.list_url()}?publication_year=1981")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Ake")

    def test_filter_by_title_exact(self):
        response = self.client.get(f"{self.list_url()}?title=No%20Longer%20at%20Ease")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["author"], self.author1.id)

    # ---------- SEARCH ----------
    def test_search_by_title_partial(self):
        response = self.client.get(f"{self.list_url()}?search=fall")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = {b["title"] for b in response.data}
        self.assertIn("Things Fall Apart", titles)

    def test_search_by_author_name_partial(self):
        response = self.client.get(f"{self.list_url()}?search=achebe")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = {b["title"] for b in response.data}
        self.assertSetEqual(titles, {"Things Fall Apart", "No Longer at Ease"})

    # ---------- ORDERING ----------
    def test_ordering_by_title_asc(self):
        response = self.client.get(f"{self.list_url()}?ordering=title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned = [b["title"] for b in response.data]
        expected = sorted([self.book1.title, self.book2.title, self.book3.title])
        self.assertEqual(returned, expected)

    def test_ordering_by_publication_year_desc(self):
        response = self.client.get(f"{self.list_url()}?ordering=-publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in response.data]
        self.assertEqual(years, sorted(years, reverse=True))
