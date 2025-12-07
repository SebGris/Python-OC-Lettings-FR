"""
Models for the lettings application.

This module defines the database models for managing rental property addresses
and lettings information.
"""
from django.db import models
from django.core.validators import MaxValueValidator, MinLengthValidator


class Address(models.Model):
    """
    Model representing a physical address.

    Attributes:
        number: Street number (1-9999).
        street: Street name.
        city: City name.
        state: Two-letter state code.
        zip_code: ZIP/postal code (up to 99999).
        country_iso_code: Three-letter ISO country code.
    """
    number = models.PositiveIntegerField(validators=[MaxValueValidator(9999)])
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    zip_code = models.PositiveIntegerField(
        validators=[MaxValueValidator(99999)]
    )
    country_iso_code = models.CharField(
        max_length=3, validators=[MinLengthValidator(3)]
    )

    class Meta:
        verbose_name_plural = "addresses"

    def __str__(self):
        """Return the street address as string representation."""
        return f"{self.number} {self.street}"


class Letting(models.Model):
    """
    Model representing a rental property letting.

    Attributes:
        title: The title/name of the letting.
        address: One-to-one relationship with an Address.
    """

    title = models.CharField(max_length=256)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    def __str__(self):
        """Return the letting title as string representation."""
        return self.title
