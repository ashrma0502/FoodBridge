from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.gis.db import models as gis_models
from apps.core.models import TimestampedModel


class User(AbstractUser, TimestampedModel):
    """
    Custom user model for FoodBridge.
    Extends AbstractUser to add role and location fields.
    """

    class Role(models.TextChoices):
        DONOR = "donor", "Donor"
        RECIPIENT = "recipient", "Recipient"
        VOLUNTEER = "volunteer", "Volunteer"
        ADMIN = "admin", "Admin"

    role = gis_models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.DONOR,
    )
    phone = gis_models.CharField(max_length=20, blank=True)
    organisation = gis_models.CharField(max_length=255, blank=True)

    # Geospatial — store the user's primary location as a point (lon, lat)
    location = gis_models.PointField(null=True, blank=True, geography=True)

    class Meta(TimestampedModel.Meta):
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})"
