"""
dispatch/models.py — Delivery route and task management.
OR-Tools will be used in dispatch/services.py to solve the VRP.
"""

from django.db import models
from django.contrib.gis.db import models as gis_models
from apps.core.models import TimestampedModel
from apps.matching.models import Match
from apps.accounts.models import User


class DeliveryRoute(TimestampedModel):
    """
    An optimised delivery route computed by OR-Tools (VRP solver).
    One route covers multiple stops for a single volunteer/driver.
    """

    class Status(models.TextChoices):
        PLANNED = "planned", "Planned"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    volunteer = gis_models.ForeignKey(
        User,
        on_delete=gis_models.PROTECT,
        related_name="routes",
        limit_choices_to={"role": User.Role.VOLUNTEER},
    )
    status = gis_models.CharField(
        max_length=20, choices=Status.choices, default=Status.PLANNED, db_index=True
    )
    total_distance_km = gis_models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    estimated_duration_minutes = gis_models.IntegerField(null=True, blank=True)
    # Serialised OR-Tools solution payload (JSON)
    route_payload = gis_models.JSONField(default=dict, blank=True)

    class Meta(TimestampedModel.Meta):
        verbose_name = "Delivery Route"
        verbose_name_plural = "Delivery Routes"

    def __str__(self):
        return f"Route #{self.pk} — {self.volunteer} [{self.status}]"


class DeliveryStop(TimestampedModel):
    """
    A single stop (pickup or drop-off) within a DeliveryRoute.
    """

    class StopType(models.TextChoices):
        PICKUP = "pickup", "Pickup"
        DROPOFF = "dropoff", "Drop-off"

    route = gis_models.ForeignKey(
        DeliveryRoute, on_delete=gis_models.CASCADE, related_name="stops"
    )
    match = gis_models.ForeignKey(
        Match, on_delete=gis_models.PROTECT, related_name="stops"
    )
    stop_type = gis_models.CharField(max_length=10, choices=StopType.choices)
    sequence = gis_models.PositiveIntegerField(
        help_text="Order of this stop within the route."
    )
    location = gis_models.PointField(geography=True)
    address = gis_models.CharField(max_length=500, blank=True)
    arrived_at = gis_models.DateTimeField(null=True, blank=True)
    completed_at = gis_models.DateTimeField(null=True, blank=True)

    class Meta(TimestampedModel.Meta):
        ordering = ["route", "sequence"]
        verbose_name = "Delivery Stop"
        verbose_name_plural = "Delivery Stops"

    def __str__(self):
        return f"Stop {self.sequence} ({self.stop_type}) on Route #{self.route_id}"
