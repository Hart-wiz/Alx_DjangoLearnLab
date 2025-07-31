# LibraryProject/urls.py

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('relationship_app.urls')),
    path('admin/', admin.site.urls),
    path('', include('relationship_app.urls')),  # Ensure this is included
]


