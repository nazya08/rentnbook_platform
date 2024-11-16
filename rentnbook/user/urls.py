from django.urls import path
from . import views
from .views import RenterProfileUpdateView, LandlordProfileUpdateView, UpdateProfileView

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('update_renter_profile/', RenterProfileUpdateView.as_view(), name='update_renter_profile'),
    path('update_landlord_profile/', LandlordProfileUpdateView.as_view(), name='update_landlord_profile'),
]
