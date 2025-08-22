# from django.db import models
# from django.contrib.auth.models import AbstractUser


# class CustomUser(AbstractUser):
#     bio = models.TextField(max_length=160, blank=True)
#     profile_picture = models.ImageField(upload_to='avatars/', blank=True, null=True)

#     # A follows B ⇒ B.followers includes A, and A.following includes B
#     followers = models.ManyToManyField(
#         'self',
#         symmetrical=False,
#         related_name='following',
#         blank=True
#     )

#     def __str__(self):
#         return self.username

#     # Follow system helpers
#     def follow(self, user):
#         """Follow another user."""
#         if user != self:
#             user.followers.add(self)

#     def unfollow(self, user):
#         """Unfollow a user."""
#         if user != self:
#             user.followers.remove(self)

#     def is_following(self, user):
#         """Check if this user is following another user."""
#         return self.following.filter(id=user.id).exists()

#     def is_followed_by(self, user):
#         """Check if this user is followed by another user."""
#         return self.followers.filter(id=user.id).exists()


from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    bio = models.TextField(max_length=160, blank=True)
    profile_picture = models.ImageField(upload_to='avatars/', blank=True, null=True)

    following = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="followers",
        blank=True
    )

    def __str__(self):
        return self.username

    def follow(self, user):
        if user != self:
            self.following.add(user)

    def unfollow(self, user):
        if user in self.following.all():
            self.following.remove(user)

    def is_following(self, user):
        return self.following.filter(id=user.id).exists()


