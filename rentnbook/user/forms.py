from django import forms
from .models import User


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    middle_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    telegram_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_picture = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}), required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'middle_name', 'telegram_name', 'profile_picture']
