from django.urls import path

from .views import AccommodationSearchView, AccommodationDetailView

urlpatterns = [
    path('search/', AccommodationSearchView.as_view(), name='accommodation_search'),
    path('<str:uuid>/', AccommodationDetailView.as_view(), name='accommodation_detail'),

]
