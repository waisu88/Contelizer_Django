from django.shortcuts import render
from django.core.exceptions import ValidationError
from .forms import PeselForm
from datetime import datetime


def check_pesel_view(request):   
    if request.method == 'POST':
        error_message = None
        form = PeselForm(request.POST)
        pesel_status = 'niepoprawny'
        sex = None
        date_of_birth = None
        if form.is_valid():
            pesel_number = form.cleaned_data['numer_pesel']
    
            year = int(pesel_number[0:2])
            month = int(pesel_number[2:4])
            day = int(pesel_number[4:6])
            
            if 0 < month < 13:
                year += 1900
            elif 20 < month < 33:
                year += 2000
                month -= 20
            elif 80 < month < 93:
                year += 1800
                month -= 80
            else:
                error_message = "Wprowadzony miesiąc w numerze PESEL jest nieprawidłowy."

            if error_message is None:
                try:
                    date_of_birth = datetime(year, month, day)
                except ValueError:
                    error_message = "Data w numerze PESEL jest nieprawidłowa."

            if error_message is None: 
                pesel_digits = [int(digit) for digit in pesel_number]
                weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
                checksum = sum(pesel_digits[i] * weights[i] for i in range(10))
                control_digit = (10 - (checksum % 10)) % 10

                if control_digit != pesel_digits[10]:
                    error_message = "Cyfra kontrolna numeru PESEL jest nieprawidłowa."
                    
            if error_message is None:
                if pesel_digits[9] % 2 == 1:
                    sex = 'mężczyzna'
                else:
                    sex = 'kobieta'
                pesel_status = 'poprawny'

            return render(request, 'pesel_results.html', {'pesel_number': pesel_number, 'pesel_status': pesel_status, 'errors': error_message, 'date_of_birth': date_of_birth, 'sex': sex})
    else:
        form = PeselForm()

    return render(request, 'pesel_form.html', {'form': form})
