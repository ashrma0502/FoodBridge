"""
core app — shared abstract models and utilities.
"""
from django.db import models


class TimestampedModel(models.Model):
    """
    Abstract base model that automatically tracks creation and update times.
    Inherit from this instead of models.Model in all FoodBridge apps.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]
