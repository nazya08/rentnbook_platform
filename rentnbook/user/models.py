import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class RolesChoices(TextChoices):
    RENTER = 'renter', _('Renter')
    LANDLORD = 'landlord', _('LandLord')
    MODERATOR = 'moderator', _('Moderator')


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=50,
        choices=RolesChoices.choices,
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', null=True, blank=True, verbose_name='Profile Picture')
    phone_number = models.CharField(max_length=20, unique=True)
    telegram_name = models.CharField(max_length=50, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    def __str__(self):
        return f"{self.email} ({self.role})"


class Renter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='renter_profile')
    rental_history = models.TextField(blank=True, null=True, help_text="History of previous rentals")
    preferred_properties = models.TextField(blank=True, null=True, help_text="Preferences for property types")

    class Meta:
        verbose_name = "Renter"
        verbose_name_plural = "Renters"

    def __str__(self):
        return f"Renter Profile for {self.user.email}"


class LandLord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='landlord_profile')
    hosting_since = models.DateField(blank=True, null=True, help_text="Date since the user started hosting")

    class Meta:
        verbose_name = "LandLord"
        verbose_name_plural = "LandLords"

    def __str__(self):
        return f"LandLord Profile for {self.user.email}"
