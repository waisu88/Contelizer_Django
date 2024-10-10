import random
from django.shortcuts import render
from .forms import TextFileUploadForm


def shuffle_word(word):
    """Shuffle the middle letters of the word, keeping the first and last letters in place."""
    if len(word) <= 3:
        return word  # Return the word as-is if it has 3 or fewer letters
    middle = list(word[1:-1])  # Get the middle letters
    random.shuffle(middle)     # Shuffle the middle letters
    return word[0] + ''.join(middle) + word[-1]  # Reconstruct the word

def process_text(text):
    """Shuffle the middle letters in each word of the text."""
    words = text.split()  # Split the text into words
    shuffled_words = [shuffle_word(word) for word in words]  # Process each word
    return ' '.join(shuffled_words)  # Join the shuffled words back into text

def upload_txt_file(request):
    if request.method == 'POST':
        form = TextFileUploadForm(request.POST, request.FILES)  # Handle file upload
        if form.is_valid():
            uploaded_file = request.FILES['file']  # Get the uploaded file
            file_bytes = uploaded_file.read()  # Read the file's content
            try:
                file_content = file_bytes.decode('utf-8')  # Try decoding as UTF-8
            except UnicodeDecodeError:
                try:
                    file_content = file_bytes.decode('ISO-8859-1')  # Try decoding as ISO-8859-1
                except UnicodeDecodeError:
                    file_content = file_bytes.decode('windows-1250')  # Fallback to windows-1250

            processed_content = process_text(file_content)  # Process the file content

            # Render the success page with processed content
            return render(request, 'upload_success.html', {'file_content': processed_content})
    else:
        form = TextFileUploadForm()  # Create a new form instance if GET request

    # Render the upload page with the form
    return render(request, 'upload.html', {'form': form})