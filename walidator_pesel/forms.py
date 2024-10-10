from django import forms
from django.core.exceptions import ValidationError


class PeselForm(forms.Form):
    pesel_number = forms.CharField(
        max_length=11,
        min_length=11,
        label="Numer PESEL",
        widget=forms.TextInput(attrs={'placeholder': 'Wprowadź 11-cyfrowy PESEL'}),
        error_messages={
            'max_length': 'Numer PESEL musi mieć dokładnie 11 cyfr.',
            'min_length': 'Numer PESEL musi mieć dokładnie 11 cyfr.',
        }
    )

    def clean_numer_pesel(self):
        pesel_number = self.cleaned_data.get('numer_pesel')
        if not pesel_number.isdigit():
            raise ValidationError("Numer PESEL może zawierać tylko cyfry.")
        return pesel_number
