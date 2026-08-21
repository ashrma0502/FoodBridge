from django.db import models
from django.contrib.gis.db import models as gis_models
from apps.core.models import TimestampedModel
from apps.accounts.models import User


class FoodListing(TimestampedModel):
    """
    A food donation listing created by a donor.
    """

    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        MATCHED = "matched", "Matched"
        IN_TRANSIT = "in_transit", "In Transit"
        DELIVERED = "delivered", "Delivered"
        EXPIRED = "expired", "Expired"
        CANCELLED = "cancelled", "Cancelled"

    donor = gis_models.ForeignKey(
        User,
        on_delete=gis_models.PROTECT,
        related_name="listings",
        limit_choices_to={"role": User.Role.DONOR},
    )
    title = gis_models.CharField(max_length=255)
    description = gis_models.TextField(blank=True)
    quantity_kg = gis_models.DecimalField(max_digits=8, decimal_places=2)
    food_type = gis_models.CharField(max_length=100, blank=True)
    expiry_datetime = gis_models.DateTimeField(null=True, blank=True)
    status = gis_models.CharField(
        max_length=20, choices=Status.choices, default=Status.AVAILABLE, db_index=True
    )

    # Geospatial — pickup location
    pickup_location = gis_models.PointField(geography=True)
    pickup_address = gis_models.CharField(max_length=500, blank=True)

    class Meta(TimestampedModel.Meta):
        verbose_name = "Food Listing"
        verbose_name_plural = "Food Listings"

    def __str__(self):
        return f"{self.title} ({self.quantity_kg} kg) — {self.status}"
