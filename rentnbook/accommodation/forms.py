from django import forms
from .models import RentalTypeChoices, Amenity, Accommodation, AccommodationPhoto


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
        label="Тип житла",
        choices=[("", "Будь-який тип")] + RentalTypeChoices.choices,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    amenities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Amenity.objects.all(),
        label="Зручності",
        widget=forms.CheckboxSelectMultiple()
    )


class AccommodationFilterForm(forms.Form):
    is_active = forms.BooleanField(required=False, label="Тільки активні", initial=True)
    rental_type = forms.ChoiceField(
        required=False,
        choices=[('', 'Усі типи')] + list(RentalTypeChoices.choices),
        label="Тип житла"
    )


class AccommodationForm(forms.ModelForm):
    class Meta:
        model = Accommodation
        fields = (
            'title', 'description', 'rental_type', 'price_per_night',
            'location', 'max_guests', 'amenities', 'available_from', 'available_to',
        )

    amenities = forms.ModelMultipleChoiceField(
        queryset=Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    available_from = forms.DateField(
        widget=forms.SelectDateWidget(years=range(2020, 2031)),
    )

    available_to = forms.DateField(
        widget=forms.SelectDateWidget(years=range(2020, 2031)),
    )

    photos = forms.FileField(
        widget=forms.TextInput(attrs={'multiple': True, "type": "File", "class": "form-control", }),
        required=False
    )
