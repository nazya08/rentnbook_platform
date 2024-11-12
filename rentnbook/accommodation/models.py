from django.db import models
from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

from common.models import TimeStampedModel


class RentalTypeChoices(TextChoices):
    APARTMENT = 'apartment', _('Apartment')
    HOUSE = 'house', _('House')
    ROOM = 'room', _('Room')


class Accommodation(TimeStampedModel):
    owner = models.ForeignKey(
        'user.LandLord', related_name='accommodations', on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    rental_type = models.CharField(choices=RentalTypeChoices, max_length=20)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.title
