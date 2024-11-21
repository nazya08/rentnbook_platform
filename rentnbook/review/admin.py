from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'accommodation_title', 'renter_name', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('accommodation__title', 'renter__user__first_name', 'renter__user__last_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    def accommodation_title(self, obj):
        return obj.accommodation.title

    accommodation_title.short_description = 'Accommodation'

    def renter_name(self, obj):
        return f"{obj.renter.user.first_name} {obj.renter.user.last_name}"

    renter_name.short_description = 'Renter'
