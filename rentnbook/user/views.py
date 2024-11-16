from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from .forms import UserUpdateForm
from .models import Renter, LandLord

User = get_user_model()


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user/profile.html'
    context_object_name = 'profile_user'

    def get_object(self, queryset=None):
        """
        Повертає поточного автентифікованого користувача.
        """
        return self.request.user

    def get_context_data(self, **kwargs):
        """
        Додає додаткові дані до контексту.
        """
        context = super().get_context_data(**kwargs)
        user = self.get_object()

        # Загальна інформація користувача
        context['full_name'] = f"{user.first_name} {user.middle_name or ''} {user.last_name}".strip()
        context['profile_picture'] = user.profile_picture
        context['telegram_name'] = user.telegram_name or 'Не вказано'

        # Додавання додаткових даних в залежності від ролі користувача
        if user.role == 'renter':
            try:
                context['renter_profile'] = user.renter_profile  # Отримуємо профіль орендаря
            except Renter.DoesNotExist:
                context['renter_profile'] = None
        elif user.role == 'landlord':
            try:
                context['landlord_profile'] = user.landlord_profile  # Отримуємо профіль власника
            except LandLord.DoesNotExist:
                context['landlord_profile'] = None

        return context


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'user/update_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Профіль успішно оновлено!')
        return response


class RenterProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Renter
    fields = ['rental_history', 'preferred_properties']
    template_name = 'profile_update.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user.renter_profile

    def form_valid(self, form):
        messages.success(self.request, 'Інформація орендаря успішно оновлена!')
        return super().form_valid(form)


class LandlordProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = LandLord
    fields = ['hosting_since']
    template_name = 'profile_update.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user.landlord_profile

    def form_valid(self, form):
        messages.success(self.request, 'Інформація орендодавця успішно оновлена!')
        return super().form_valid(form)
