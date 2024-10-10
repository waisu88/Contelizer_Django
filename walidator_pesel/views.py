from django.shortcuts import render
from django.core.exceptions import ValidationError
from .forms import PeselForm
from datetime import datetime

def check_pesel_view(request):   
    if request.method == 'POST':  # Check if the request is a POST
        error_message = None
        form = PeselForm(request.POST)  # Instantiate the form with POST data
        pesel_status = 'niepoprawny'  # Default status for PESEL
        sex = None  # Variable to hold gender
        date_of_birth = None  # Variable to hold date of birth
        
        if form.is_valid():  # Validate the form
            pesel_number = form.cleaned_data['pesel_number']  # Get the validated PESEL number
    
            year = int(pesel_number[0:2])  # Extract year from PESEL
            month = int(pesel_number[2:4])  # Extract month from PESEL
            day = int(pesel_number[4:6])  # Extract day from PESEL
            
            # Determine the correct year based on the month value
            if 0 < month < 13:
                year += 1900
            elif 20 < month < 33:
                year += 2000
                month -= 20
            elif 80 < month < 93:
                year += 1800
                month -= 80
            else:
                error_message = "Wprowadzony miesiąc w numerze PESEL jest nieprawidłowy."  # Invalid month

            if error_message is None:  # If no errors so far
                try:
                    date_of_birth = datetime(year, month, day)  # Validate the date
                except ValueError:
                    error_message = "Data w numerze PESEL jest nieprawidłowa."  # Invalid date

            if error_message is None:  # Proceed if still no errors
                pesel_digits = [int(digit) for digit in pesel_number]  # Convert PESEL to list of digits
                weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]  # Weights for checksum calculation
                checksum = sum(pesel_digits[i] * weights[i] for i in range(10))  # Calculate checksum
                control_digit = (10 - (checksum % 10)) % 10  # Calculate control digit

                if control_digit != pesel_digits[10]:  # Validate control digit
                    error_message = "Cyfra kontrolna numeru PESEL jest nieprawidłowa."  # Invalid control digit
                  
            if error_message is None:  # No errors, determine sex and status
                if pesel_digits[9] % 2 == 1:  # Determine gender based on the 10th digit
                    sex = 'mężczyzna'
                else:
                    sex = 'kobieta'
                pesel_status = 'poprawny'  # Set status to valid

            # Render the results page with the provided data
            return render(request, 'pesel_results.html', {
                'pesel_number': pesel_number,
                'pesel_status': pesel_status,
                'errors': error_message,
                'date_of_birth': date_of_birth,
                'sex': sex
            })
    else:
        form = PeselForm()  # Instantiate an empty form for GET requests

    return render(request, 'pesel_form.html', {'form': form})  # Render the form page
