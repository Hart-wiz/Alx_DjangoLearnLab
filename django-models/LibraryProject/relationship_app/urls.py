# from django.urls import path
# from .views import list_books, LibraryDetailView, Register_view
# from django.contrib.auth.views import LoginView, LogoutView
# from . import admin_view, librarian_view, member_view

# urlpatterns = [
#     path('books/', list_books, name='list_books'),
#     path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
#     path('login/', LoginView.as_view(template_name='login.html'), name='login'),
#     path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
#     path('register/', Register_view.as_view(), name='register'),
#     path('admin-role/', admin_view.admin_view, name='admin_view'),
#     path('librarian-role/', librarian_view.librarian_view, name='librarian_view'),
#     path('member-role/', member_view.member_view, name='member_view'),
# ]


from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from . import admin_view, librarian_view, member_view

urlpatterns = [
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    
    # Fix: use template_name
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),

    # Fix: use views.register (a function), not Register_view.as_view()
    path('register/', views.register, name='register'),

    path('admin-role/', admin_view.admin_view, name='admin_view'),
    path('librarian-role/', librarian_view.librarian_view, name='librarian_view'),
    path('member-role/', member_view.member_view, name='member_view'),
    
    
    path('books/add/', views.add_book, name='add-book'),
    path('books/edit/<int:pk>/', views.edit_book, name='edit-book'),
    path('books/delete/<int:pk>/', views.delete_book, name='delete-book')
]



