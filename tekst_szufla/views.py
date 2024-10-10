import random
from django.shortcuts import render
from .forms import TextFileUploadForm


def shuffle_word(word):
    """Mieszaj środkowe litery słowa, zostawiając pierwszą i ostatnią na miejscu."""
    if len(word) <= 3:
        return word
    middle = list(word[1:-1])  # Pobierz środkowe litery
    random.shuffle(middle)     # Wymieszaj je
    return word[0] + ''.join(middle) + word[-1]  # Złóż słowo

def process_text(text):
    """Mieszaj środkowe litery w każdym słowie."""
    words = text.split()  # Podziel tekst na słowa
    shuffled_words = [shuffle_word(word) for word in words]  # Przetwarzaj każde słowo
    return ' '.join(shuffled_words)  # Scal z powrotem w tekst

def upload_txt_file(request):
    if request.method == 'POST':
        form = TextFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            file_bytes = uploaded_file.read()
            try:
                file_content = file_bytes.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    file_content = file_bytes.decode('ISO-8859-1') 
                except UnicodeDecodeError:
                    file_content = file_bytes.decode('windows-1250')

            processed_content = process_text(file_content)

            return render(request, 'upload_success.html', {'file_content': processed_content})
    else:
        form = TextFileUploadForm()

    return render(request, 'upload.html', {'form': form})