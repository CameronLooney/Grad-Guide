
from rake_nltk import Rake
import string
import io
import PyPDF2
import re


def keyphrases(file, min_word, max_word, num_phrases):
    text = file
    text = text.lower()
    text = ''.join(s for s in text if ord(s) > 31 and ord(s) < 126)
    text = text
    text = re.sub(' +', ' ', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = ''.join([i for i in text if not i.isdigit()])
    r = Rake(min_length=min_word, max_length=max_word)
    r.extract_keywords_from_text(text)
    phrases = r.get_ranked_phrases()

    if num_phrases < len(phrases):
        phrases = phrases[0:num_phrases]

    return phrases

def process_resume(uploaded_file,num_phrases):
    file_text = ''
    phrases = []
    uploaded_file.seek(0)
    file = uploaded_file.read()
    pdf = PyPDF2.PdfFileReader(io.BytesIO(file))

    for page in range(pdf.getNumPages()):
        file_text += (pdf.getPage(page).extractText())
        phrases.extend(keyphrases(file_text, 1, 3, num_phrases))

    return phrases