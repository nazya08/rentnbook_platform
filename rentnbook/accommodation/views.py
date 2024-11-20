from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView

from .models import Accommodation, AccommodationPhoto
from .forms import AccommodationSearchForm, AccommodationForm, AccommodationFilterForm


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

            # Сортуємо за обраним полем
            sort_by = form.cleaned_data.get("sort_by")
            if sort_by:
                queryset = queryset.order_by(sort_by)

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


class MyAccommodationsView(LoginRequiredMixin, ListView):
    model = Accommodation
    template_name = 'accommodation/my_accommodations.html'
    context_object_name = 'accommodations'
    paginate_by = 6

    def get_queryset(self):
        """Повертає тільки житло, що належить поточному користувачеві, з можливістю фільтрації."""
        queryset = Accommodation.objects.filter(owner__user=self.request.user).order_by('-created_at')

        is_active = self.request.GET.get('is_active', None)
        rental_type = self.request.GET.get('rental_type', None)

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active == 'on')

        if rental_type:
            queryset = queryset.filter(rental_type=rental_type)

        return queryset

    def get_context_data(self, **kwargs):
        """Додаємо форму фільтрації до контексту."""
        context = super().get_context_data(**kwargs)
        context['form'] = AccommodationFilterForm(self.request.GET)
        return context


def create_accommodation(request):
    form = AccommodationForm()

    if request.method == 'POST':
        form = AccommodationForm(request.POST)
        photos = request.FILES.getlist('photos')
        print(photos)
        if form.is_valid():
            accommodation = form.save(commit=False)
            accommodation.owner = request.user.landlord_profile
            accommodation.save()

            form.save_m2m()

            for photo in photos:
                AccommodationPhoto.objects.create(accommodation=accommodation, photo=photo)

            messages.success(request, 'Ваше житло успішно створено!')
            return redirect('my_accommodations')
        else:
            messages.error(request, 'Будь ласка, виправте помилки нижче.')

    return render(
        request,
        'accommodation/accommodation_create.html',
        {'form': form, }
    )


class AccommodationUpdateView(LoginRequiredMixin, UpdateView):
    model = Accommodation
    fields = ['title', 'description', 'price_per_night', 'location', 'max_guests', 'available_from', 'available_to']
    template_name = 'accommodation/update_accommodation.html'
    success_url = reverse_lazy('my_accommodations')

    def get_object(self, queryset=None):
        return get_object_or_404(Accommodation, uuid=self.kwargs['uuid'])

    def get_queryset(self):
        # Переконайтеся, що користувач може оновлювати тільки своє житло
        return Accommodation.objects.filter(owner__user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner.user != request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

