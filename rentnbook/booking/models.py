from django.db import models
from django.utils.translation import gettext_lazy as _

from accommodation.models import Accommodation
from common.models import TimeStampedModel
from user.models import Renter


class BookingStatusChoices(models.TextChoices):
    PENDING = 'pending', _('Pending')
    CONFIRMED = 'confirmed', _('Confirmed')
    CANCELLED = 'cancelled', _('Cancelled')


class Booking(TimeStampedModel):
    renter = models.ForeignKey(Renter, on_delete=models.CASCADE, related_name='bookings')
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=BookingStatusChoices.choices,
        default=BookingStatusChoices.PENDING
    )

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        unique_together = ('renter', 'accommodation', 'start_date', 'end_date')

    def __str__(self):
        return f"Booking #{self.uuid} by {self.renter.user.email} for {self.accommodation.title} from {self.start_date} to {self.end_date}"
