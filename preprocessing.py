import pandas as pd
import nltk
import string

nltk.download('stopwords')

from nltk.corpus import stopwords

def clean_text(text):

    text = text.lower()

    text = ''.join(
        ch for ch in text
        if ch not in string.punctuation
    )

    words = text.split()

    words = [
        word for word in words
        if word not in stopwords.words('english')
    ]

    return " ".join(words)