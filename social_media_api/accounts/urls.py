
from django.urls import path
from .views import RegisterView, LoginView, ProfileView

urlpatterns = [
    # both with and without trailing slash for convenience
    path('register', RegisterView.as_view(), name='register'),
    path('register/', RegisterView.as_view()),
    path('login', LoginView.as_view(), name='login'),
    path('login/', LoginView.as_view()),
    path('profile', ProfileView.as_view(), name='profile'),
    path('profile/', ProfileView.as_view()),
]
