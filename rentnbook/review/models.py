from django.db import models

from accommodation.models import Accommodation
from common.models import TimeStampedModel
from user.models import Renter


class Review(TimeStampedModel):
    accommodation = models.ForeignKey(Accommodation, related_name="reviews", on_delete=models.CASCADE)
    renter = models.ForeignKey(Renter, related_name="reviews", on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Review by {self.renter.user.first_name} {self.renter.user.last_name} for {self.accommodation.title}"

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        unique_together = ('accommodation', 'renter')
        ordering = ['created_at']
