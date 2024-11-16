from django import forms
from .models import RentalTypeChoices, Amenity


class AccommodationSearchForm(forms.Form):
    location = forms.CharField(
        required=False,
        label="Місцезнаходження",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    available_from = forms.DateField(
        required=False,
        label="Доступно з",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    available_to = forms.DateField(
        required=False,
        label="Доступно до",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    max_guests = forms.IntegerField(
        required=False,
        label="Кількість гостей",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    rental_type = forms.ChoiceField(
        required=False,
        label="Тип оренди",
        choices=[("", "Будь-який тип")] + RentalTypeChoices.choices,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    amenities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Amenity.objects.all(),
        label="Зручності",
        widget=forms.CheckboxSelectMultiple()
    )
