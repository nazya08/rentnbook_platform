from django.db import models
from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

from common.models import TimeStampedModel


class RentalTypeChoices(TextChoices):
    APARTMENT = 'apartment', _('Apartment')
    HOUSE = 'house', _('House')
    ROOM = 'room', _('Room')


class Amenity(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Amenity"
        verbose_name_plural = "Amenities"

    def __str__(self):
        return self.name


class Accommodation(TimeStampedModel):
    owner = models.ForeignKey(
        'user.LandLord', related_name='accommodations', on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    rental_type = models.CharField(choices=RentalTypeChoices.choices, max_length=20)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    max_guests = models.PositiveIntegerField()
    amenities = models.ManyToManyField(Amenity, blank=True, related_name="accommodations")
    available_from = models.DateField()
    available_to = models.DateField()

    class Meta:
        verbose_name = "Accommodation"
        verbose_name_plural = "Accommodations"

    def __str__(self):
        return f'Accommodation #{self.uuid}'


class AccommodationPhoto(models.Model):
    accommodation = models.ForeignKey(
        Accommodation, related_name='photos', on_delete=models.CASCADE
    )
    photo = models.ImageField(upload_to='accommodation_photos/')
    caption = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Accommodation Photo"
        verbose_name_plural = "Accommodation Photos"

    def __str__(self):
        return f"Photo of {self.accommodation.title}"
