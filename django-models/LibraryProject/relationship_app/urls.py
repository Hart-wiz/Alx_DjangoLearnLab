# relationship_app/urls.py

from . import views
from django.urls import path
from .views import list_books, LibraryDetailView
from . import admin_view, librarian_view, member_view

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('admin-role/', admin_view.admin_view, name='admin_view'),
    path('librarian-role/', librarian_view.librarian_view, name='librarian_view'),
    path('member-role/', member_view.member_view, name='member_view'),
]


