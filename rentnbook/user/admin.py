from django.contrib import admin
from .models import User, Renter, LandLord


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('role', 'is_active', 'is_staff')
    ordering = ('-date_joined',)


@admin.register(Renter)
class RenterAdmin(admin.ModelAdmin):
    list_display = ('user', 'rental_history', 'preferred_properties')
    search_fields = ('user__email', 'rental_history')
    list_filter = ('user__role',)
    ordering = ('user__email',)


@admin.register(LandLord)
class LandLordAdmin(admin.ModelAdmin):
    list_display = ('user', 'hosting_since',)
    search_fields = ('user__email',)
    list_filter = ('user__role',)
    ordering = ('user__email',)

    # TODO: add count of properties owned

    # def properties_owned_count(self, obj):
    #     return obj.properties_owned.count()
    #
    # properties_owned_count.short_description = 'Properties Owned'
