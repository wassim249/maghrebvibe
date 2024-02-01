import pandas as pd
import re
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from unidecode import unidecode

import nltk
nltk.download('punkt')
nltk.download('stopwords')

# Charger le fichier CSV
df = pd.read_csv('C:\Users\21270\maghrebvibe\maghrebvibe\darija_reviews.csv')

# Fonction pour nettoyer le texte
def clean_text(text):
    # Supprimer les balises HTML
    text = re.sub(r'<.*?>', '', text)
    # Supprimer les caractères spéciaux et les liens
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    # Tokeniser le texte en phrases et ensuite en mots
    tokens = word_tokenize(text)
    # Supprimer les stop words et normaliser le texte
    stop_words = set(stopwords.words('arabic'))  # Vous pouvez ajuster la langue ici
    tokens = [word for word in tokens if word.lower() not in stop_words]
    # Normaliser le texte (minuscules, suppression des accents)
    tokens = [unidecode(word.lower()) for word in tokens]
    return ' '.join(tokens)

# Appliquer la fonction de nettoyage sur la colonne 'review'
df['cleaned_review'] = df['review'].apply(clean_text)

# Imprimer le résultat
print(df[['review', 'cleaned_review', 'rating', 'sentiment']])

df[['cleaned_review', 'rating', 'sentiment']].to_csv('darija_reviews_cleaned.csv', index=False)
