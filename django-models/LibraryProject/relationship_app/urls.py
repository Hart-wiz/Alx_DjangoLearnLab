# relationship_app/urls.py

from . import views
from django.urls import path
from . import admin_view, librarian_view, member_view
from .views import (
    list_books, LibraryDetailView,
    LoginView, LogoutView, Register_view
)
from . import admin_view, librarian_view, member_view



urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', Register_view.as_view(), name='register'),
    path('admin-role/', admin_view.admin_view, name='admin_view'),
    path('librarian-role/', librarian_view.librarian_view, name='librarian_view'),
    path('member-role/', member_view.member_view, name='member_view'),
]

