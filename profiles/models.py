"""
Models for the profiles application.

This module defines the database models for user profile management.
"""
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Model representing a user profile.

    Extends the built-in User model with additional information.

    Attributes:
        user: One-to-one relationship with Django's User model.
        favorite_city: The user's favorite city (optional).
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_city = models.CharField(max_length=64, blank=True)

    def __str__(self):
        """Return the username as string representation."""
        return self.user.username
