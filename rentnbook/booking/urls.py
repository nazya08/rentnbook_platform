from django.urls import path
from .views import BookingCreateView, MyBookingsView, BookingDetailView, RentRequestsView, ActiveBookingsView, \
    cancel_booking

urlpatterns = [
    path('<uuid:uuid>/', BookingDetailView.as_view(), name='booking_detail'),
    path('accommodation/<uuid:uuid>/', BookingCreateView.as_view(), name='create_booking'),
    path('cancel/accommodation/<uuid:uuid>/', cancel_booking, name='cancel_booking'),
    path('my_bookings/', MyBookingsView.as_view(), name='my_bookings'),
    path('active-bookings/', ActiveBookingsView.as_view(), name='active_bookings'),
    path('rent-requests/', RentRequestsView.as_view(), name='rent_requests'),
]
