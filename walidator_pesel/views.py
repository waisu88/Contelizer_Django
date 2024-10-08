from django.shortcuts import render
from .forms import PeselForm


def pesel_view(request):
    if request.method == 'POST':
        form = PeselForm(request.POST)
        if form.is_valid():
            numer_pesel = form.cleaned_data['numer_pesel']
            # błąd jeśli jest większe od 20 i mniejsze od 33 ale 4:6 jest większe od 24
            print(numer_pesel[2:4])
            # musi być większe od 0 i mniejsze od 13
            # lub większe od 20 i mniejsze od 33
            # lub większe od 80 i mniejsze od 83
            print(numer_pesel[4:6])
            # rok 1900 nie jest przestępny, 2000 już jest
            # czyli jeśli 008 albo 009 to musimy sprawdzić czy liczba dni w lutym się zgadza
            # trzeba sprawdzić, ktore miesiące ile mają dni i napisac logikę
            # trzeba sprawdzić sumę kontrolną ze wzoru jako ostateczną

            # ostatni krok to przekazanie daty urodzenia i płci do widoku

            # może najbardziej odpowiednim podejściem jest rozbicie tego według miesięcy..?


            return render(request, 'success.html', {'pesel': numer_pesel})
    else:
        form = PeselForm()

    return render(request, 'pesel_form.html', {'form': form})
