from django.contrib import admin
from .models import Accommodation, Amenity, AccommodationPhoto


@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'owner', 'rental_type', 'price_per_night', 'location', 'created_at', 'available_from', 'available_to')
    search_fields = ('title', 'owner__user__email', 'location')
    list_filter = ('rental_type', 'available_from', 'available_to')
    ordering = ('-created_at',)
    filter_horizontal = ('amenities',)
    date_hierarchy = 'created_at'
    list_select_related = ('owner',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(AccommodationPhoto)
class AccommodationPhotoAdmin(admin.ModelAdmin):
    list_display = ('accommodation', 'caption')
    search_fields = ('accommodation__title', 'caption')
    ordering = ('accommodation',)

    def accommodation_title(self, obj):
        return obj.accommodation.title

    accommodation_title.short_description = 'Accommodation Title'
