import re

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from user.models import RolesChoices

User = get_user_model()


class SignupForm(forms.ModelForm):
    """
    Форма для реєстрації нового користувача.
    """
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ім\'я'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Прізвище'}))
    middle_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'По-батькові'}), required=False
    )
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон'}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Електронна пошта'})
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторний пароль'})
    )

    role = forms.ChoiceField(choices=RolesChoices.choices,
                             widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        """
        Модель форми з полями.
        """
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'phone_number', 'email', 'role', 'password', 'password2',)

    def clean_phone_number(self):
        """
        Перевірка, чи існує вже користувач з таким номером телефону.
        """
        phone_number = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("Користувач з таким номером телефону вже існує.")
        return phone_number

    def clean_email(self):
        """
        Перевірка, чи існує вже користувач з такою поштою.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Користувач з такою поштою вже існує.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 8:
            raise ValidationError("Пароль повинен містити щонайменше 8 символів.")

        if not re.search(r'\d', password):
            raise ValidationError("Пароль повинен містити хоча б одну цифру.")

        if not re.search(r'[A-Z]', password):
            raise ValidationError("Пароль повинен містити хоча б одну велику літеру.")

        if not re.search(r'[a-z]', password):
            raise ValidationError("Пароль повинен містити хоча б одну малу літеру.")

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            self.add_error('password2', "Паролі не співпадають")


class LoginForm(forms.Form):
    """
    Форма авторизації.
    """
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Електронна пошта'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))
