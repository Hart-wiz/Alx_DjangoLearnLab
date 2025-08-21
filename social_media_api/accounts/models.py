from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    bio = models.CharField(max_length=160, blank=True)
    profile_picture = models.ImageField(upload_to='avatars/', blank=True, null=True)
    # A follows B  ⇒  B.followers includes A, and A.following includes B
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True
    )

    def __str__(self):
        return self.username
