from django.urls import path

from .views import AccommodationSearchView, AccommodationDetailView, MyAccommodationsView, AccommodationUpdateView, \
    create_accommodation

urlpatterns = [
    path('search/', AccommodationSearchView.as_view(), name='accommodation_search'),
    path('my-accommodations/', MyAccommodationsView.as_view(), name='my_accommodations'),
    path('add/', create_accommodation, name='accommodation_create'),
    path('<uuid:uuid>/', AccommodationDetailView.as_view(), name='accommodation_detail'),
    path('<uuid:uuid>/update/', AccommodationUpdateView.as_view(), name='accommodation_update'),
]
