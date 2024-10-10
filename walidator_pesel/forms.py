from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class PeselForm(forms.Form):
    # Create a regex validator that allows only digits (0-9)
    digit_validator = RegexValidator(
        regex=r'^\d{11}$',  # Ensure the string contains exactly 11 digits
        message="Numer PESEL może zawierać tylko cyfry i musi mieć dokładnie 11 cyfr."
    )
    
    pesel_number = forms.CharField(
        label="Numer PESEL",
        widget=forms.TextInput(attrs={'placeholder': 'Wprowadź 11-cyfrowy PESEL'}),
        validators=[digit_validator],  # Add the digit validator
        error_messages={
            'max_length': 'Numer PESEL musi mieć dokładnie 11 cyfr.',
            'min_length': 'Numer PESEL musi mieć dokładnie 11 cyfr.',
        },
        max_length=11,
        min_length=11,
    )
