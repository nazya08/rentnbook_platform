from django import forms
from django.core.exceptions import ValidationError

from .models import Booking


class BookingForm(forms.ModelForm):
    #Форма для створення або редагування бронювання.

    class Meta:
        model = Booking
        fields = ('start_date', 'end_date', 'guests',)

        # Налаштування віджетів для кожного поля
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'guests': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

        # Мітки для полів
        labels = {
            'start_date': 'Дата заїзду',
            'end_date': 'Дата виїзду',
            'guests': 'Кількість гостей',
        }

    def __init__(self, *args, **kwargs):
        self.accommodation = kwargs.pop('accommodation', None)  # Отримуємо житло
        super().__init__(*args, **kwargs)

        # Додаємо атрибути "min" і "max" до віджетів дати
        if self.accommodation:
            self.fields['start_date'].widget.attrs.update({
                'min': self.accommodation.available_from.isoformat(),
                'max': self.accommodation.available_to.isoformat(),
            })
            self.fields['end_date'].widget.attrs.update({
                'min': self.accommodation.available_from.isoformat(),
                'max': self.accommodation.available_to.isoformat(),
            })

    def clean(self):
        # Валідатор для перевірки коректності введених даних.
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        # Перевірка на наявність житла
        if not self.accommodation:
            raise ValidationError("Не вдалося знайти житло.")

        # Перевірка діапазону дат доступності
        if start_date < self.accommodation.available_from or end_date > self.accommodation.available_to:
            raise ValidationError(
                f"Дати мають бути в межах доступності житла: з {self.accommodation.available_from} до {self.accommodation.available_to}.")

        return cleaned_data
