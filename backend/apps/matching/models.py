from django.db import models
from apps.core.models import TimestampedModel
from apps.listings.models import FoodListing
from apps.accounts.models import User


class Match(TimestampedModel):
    """
    Records a pairing between a food listing and a recipient organisation.
    """

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"
        COMPLETED = "completed", "Completed"

    listing = models.ForeignKey(
        FoodListing, on_delete=models.CASCADE, related_name="matches"
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="matches",
        limit_choices_to={"role": User.Role.RECIPIENT},
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True
    )
    score = models.FloatField(
        null=True,
        blank=True,
        help_text="Matching score computed by the matching algorithm.",
    )
    notes = models.TextField(blank=True)

    class Meta(TimestampedModel.Meta):
        verbose_name = "Match"
        verbose_name_plural = "Matches"
        unique_together = [("listing", "recipient")]

    def __str__(self):
        return f"Match({self.listing_id} → {self.recipient_id}) [{self.status}]"
