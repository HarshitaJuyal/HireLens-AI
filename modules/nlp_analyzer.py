import nltk
import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


# Download required NLTK data
nltk.download('punkt_tab')
nltk.download('stopwords')


def clean_text(text):

    # Convert text to lowercase
    text = text.lower()

    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # Tokenize words
    words = word_tokenize(text)

    # Remove stopwords
    filtered_words = [
        word for word in words
        if word not in stopwords.words('english')
    ]

    return filtered_words