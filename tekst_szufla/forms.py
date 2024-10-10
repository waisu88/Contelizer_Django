from django import forms
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    valid_extensions = ['.txt']
    if not any(value.name.endswith(ext) for ext in valid_extensions):
        raise ValidationError('Nieprawidłowy typ pliku. Dozwolone rozszerzenia: .txt')

class TextFileUploadForm(forms.Form):
    file = forms.FileField(label='Wybierz plik tekstowy', validators=[validate_file_extension])
