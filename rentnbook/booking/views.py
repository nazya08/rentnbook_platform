from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from .forms import BookingForm
from .models import Booking, Accommodation, BookingStatusChoices


class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = "booking/create_booking.html"
    success_url = reverse_lazy('my_bookings')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        accommodation = get_object_or_404(Accommodation, uuid=self.kwargs['uuid'])
        kwargs['accommodation'] = accommodation  # Передаємо житло у форму
        return kwargs

    def form_valid(self, form):
        accommodation = get_object_or_404(Accommodation, uuid=self.kwargs['uuid'])
        form.instance.accommodation = accommodation
        form.instance.renter = self.request.user.renter_profile

        # Перевірка кількості гостей
        if form.cleaned_data['guests'] > accommodation.max_guests:
            # Додаємо помилку до форми
            form.add_error('guests',
                           f"Кількість гостей перевищує максимум для цього житла ({accommodation.max_guests} гостей).")
            return self.form_invalid(form)

        # Перевірка доступності дат у формі (якщо потрібно)
        if Booking.objects.filter(
                accommodation=accommodation,
                start_date__lt=form.cleaned_data['end_date'],
                end_date__gt=form.cleaned_data['start_date'],
                status=BookingStatusChoices.CONFIRMED
        ).exists():
            form.add_error('start_date', 'Ці дати вже заброньовані!')
            return self.form_invalid(form)

        # Перевірка доступності дат у формі
        return super().form_valid(form)


class MyBookingsView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = "booking/my_bookings.html"
    context_object_name = "bookings"
    login_url = "login"

    def get_queryset(self):
        status_filter = self.request.GET.get('status', None)
        queryset = Booking.objects.filter(renter=self.request.user.renter_profile).order_by('-created_at')

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset


def cancel_booking(request, uuid):
    booking = get_object_or_404(Booking, uuid=uuid)

    if booking.renter != request.user.renter_profile:  # Перевірка чи бронювання належить цьому користувачу
        messages.error(request, "Ви не можете скасувати це бронювання.")
        return redirect('my_bookings')

    if booking.status != BookingStatusChoices.PENDING:
        messages.error(request, "Це бронювання не можна скасувати.")
        return redirect('my_bookings')

    booking.status = BookingStatusChoices.CANCELLED
    booking.is_active = False
    booking.save()
    messages.success(request, "Бронювання було скасоване.")
    return redirect('my_bookings')


class BookingDetailView(DetailView):
    model = Booking
    template_name = 'booking/booking_detail.html'
    context_object_name = 'booking'

    def get_object(self, queryset=None):
        """
        Отримуємо бронювання за uuid з URL. Якщо бронювання не належить
        поточному користувачу, перенаправляємо на список бронювань.
        """
        booking = get_object_or_404(Booking, uuid=self.kwargs['uuid'])

        # Перевірка, чи належить бронювання поточному користувачу
        if booking.renter != self.request.user.renter_profile:
            messages.error(self.request, "Це бронювання не належить вам.")
            return redirect('my_bookings')

        return booking


class RentRequestsView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = "booking/rent_requests.html"
    context_object_name = "bookings"
    login_url = "login"

    def get_queryset(self):
        return Booking.objects.filter(accommodation__owner=self.request.user.landlord_profile, status='pending')

    def post(self, request, *args, **kwargs):
        booking_uuid = request.POST.get('booking_uuid')
        action = request.POST.get('action')

        if booking_uuid and action in ['confirm', 'reject']:
            booking = Booking.objects.get(uuid=booking_uuid)
            if action == 'confirm':
                booking.status = 'confirmed'
            elif action == 'reject':
                booking.status = 'cancelled'
            booking.save()

        return redirect('rent_requests')


class ActiveBookingsView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'booking/active_bookings.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        # Фільтруємо бронювання за житлом, яке належить поточному користувачеві
        return Booking.objects.filter(
            accommodation__owner=self.request.user.landlord_profile,
            status=BookingStatusChoices.CONFIRMED,
            is_active=True,
        )
