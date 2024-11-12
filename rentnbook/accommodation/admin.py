from django.contrib import admin
from .models import Accommodation


@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'rental_type', 'price_per_night', 'location', 'created_at')
    search_fields = ('title', 'owner__email', 'location')
    list_filter = ('rental_type',)
    ordering = ('-created_at',)
