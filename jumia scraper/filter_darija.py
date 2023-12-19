import pandas as pd
from transformers import pipeline
import os
import json

def filter_darija_sentences(file_path):
    # Read sentences from CSV and filter Darija sentences
    reviews_csv = pd.read_csv(file_path)
    reviews = reviews_csv['review'].values.astype(str).tolist()

    if os.path.exists('results.json'):
       with open('results.json','r',encoding='utf-8') as f:
          results = json.load(f)
    else:
      # Initialize the language detection pipeline
      language_pipe = pipeline("text-classification", model="papluca/xlm-roberta-base-language-detection")
      results = language_pipe(reviews)
      with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f)

    # Filter Darija sentences based on the language detection score
    darija_sentences = [reviews[idx] if result['score'] < 0.98 else None for idx, result in enumerate(results)]

    

    # Create a new dataframe for Darija sentences
    darija_sentences_df = pd.DataFrame(columns=['review', 'rating','sentiment'])
    
    darija_sentences_df['review'] = darija_sentences
    darija_sentences_df['rating'] = reviews_csv['rating'].where(reviews_csv['review'].isin(darija_sentences), None)
    darija_sentences_df['sentiment'] = darija_sentences_df['rating'].apply(lambda x: 'negative' if x < 3 else 'positive')
    
    # Filter out None values
    darija_sentences_df.dropna(inplace=True)
    

    # Save the new dataframe to a csv file
    darija_sentences_df.to_csv('darija_reviews.csv', index=False)
