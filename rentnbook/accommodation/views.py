from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Accommodation
from .forms import AccommodationSearchForm
from django.db.models import Q


class AccommodationSearchView(ListView):
    model = Accommodation
    template_name = "accommodation/accommodation_search.html"
    context_object_name = "accommodations"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        form = self.get_search_form()

        if form.is_valid():
            # Фільтруємо за місцезнаходженням
            location = form.cleaned_data.get("location")
            if location:
                queryset = queryset.filter(location__icontains=location)

            # Фільтруємо за датами
            available_from = form.cleaned_data.get("available_from")
            available_to = form.cleaned_data.get("available_to")
            if available_from:
                queryset = queryset.filter(available_to__gte=available_from)
            if available_to:
                queryset = queryset.filter(available_from__lte=available_to)

            # Фільтруємо за кількістю гостей
            max_guests = form.cleaned_data.get("max_guests")
            if max_guests:
                queryset = queryset.filter(max_guests__gte=max_guests)

            # Фільтруємо за типом оренди
            rental_type = form.cleaned_data.get("rental_type")
            if rental_type:
                queryset = queryset.filter(rental_type=rental_type)

            # Фільтруємо за зручностями
            amenities = form.cleaned_data.get("amenities")
            if amenities:
                for amenity in amenities:
                    queryset = queryset.filter(amenities=amenity)

        return queryset.distinct()

    def get_search_form(self):
        return AccommodationSearchForm(self.request.GET or None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_search_form()
        return context


class AccommodationDetailView(DetailView):
    model = Accommodation
    template_name = "accommodation/accommodation_detail.html"
    context_object_name = "accommodation"

    def get_object(self, queryset=None):
        return get_object_or_404(Accommodation, uuid=self.kwargs['uuid'])

