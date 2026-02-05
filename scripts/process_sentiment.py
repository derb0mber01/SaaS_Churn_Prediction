import pandas as pd
import os
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Initialize and Update Lexicon
nltk.download('vader_lexicon', quiet=True)
analyzer = SentimentIntensityAnalyzer()

# CUSTOM TUNING: Tell the AI that these SaaS-specific terms are negative
new_words = {
    'increased': -2.0, # In support, price 'increased' is usually bad
    'limit': 0.0,      # Ensure 'limit' doesn't sway positive
    'pricing': -1.5,   # Focus on cost complaints
}
analyzer.lexicon.update(new_words)

def process_sentiment():
    data_dir = r"C:\Users\uduok\git_folder\SaaS_Churn_Prediction\data\raw"
    df = pd.read_csv(os.path.join(data_dir, 'fact_support_tickets.csv'))

    # calculate Sentiment with tuned Lexicon
    df['sentiment_score'] = df['ticket_text'].apply(
        lambda x: analyzer.polarity_scores(str(x))['compound']
    )

    # Align Priority with Sentiment
    # If sentiment is very negative (< -0.3), force High Priority
    df.loc[df['sentiment_score'] < -0.3, 'priority'] = 'High'
    # If sentiment is positive or neutral, force Low Priority
    df.loc[df['sentiment_score'] >= -0.1, 'priority'] = 'Low'

    # 4. Tighten Neutral Labels
    def label_sentiment(score):
        if score > 0.2: return 'Positive'   # Higher bar for positive
        elif score < -0.1: return 'Negative' # More sensitive to negative
        else: return 'Neutral'

    df['sentiment_label'] = df['sentiment_score'].apply(label_sentiment)

    # Remove duplicates per customer
    # Ensure a customer doesn't send the exact same praise 4 times
    df = df.drop_duplicates(subset=['customer_id', 'ticket_text'])

    df.to_csv(os.path.join(data_dir, 'fact_support_tickets_scored.csv'), index=False)
    print("Tuned Sentiment Analysis Complete: Duplicates removed and Priority aligned.")

if __name__ == "__main__":
    process_sentiment()
