from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('renter_email', 'accommodation_title', 'start_date', 'end_date', 'status', 'created_at')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('renter__user__email', 'accommodation__title')
    ordering = ('-created_at', 'start_date')
    date_hierarchy = 'start_date'
    readonly_fields = ('created_at', 'updated_at')

    def renter_email(self, obj):
        return obj.renter.user.email

    renter_email.short_description = 'Renter Email'

    def accommodation_title(self, obj):
        return obj.accommodation.title

    accommodation_title.short_description = 'Accommodation Title'
