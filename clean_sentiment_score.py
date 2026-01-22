#!/usr/bin/env python
import pandas as pd
import os

# directory setup
data_dir = r"C:\Users\uduok\git_folder\SaaS_Churn_Prediction\data"
file_path = os.path.join(data_dir, 'fact_support_tickets_scored.csv')

def clean_sentiment_scores():
    df = pd.read_csv(file_path)

    # match scores to labels if they are inconsistent
    def sync_score(row):
        label = str(row['sentiment_label']).strip().capitalize()
        score = row['sentiment_score']
        
        if label == 'Negative' and score > -0.1:
            return -0.75  # Force to a clear negative value
        if label == 'Positive' and score < 0.1:
            return 0.75   # Force to a clear positive value
        if label == 'Neutral':
            return 0.0    # Force pure neutral
        return score

    print("Syncing numerical scores with manual labels...")
    df['sentiment_score'] = df.apply(sync_score, axis=1)

    # save the finalized version
    df.to_csv(file_path, index=False)
    print(f"Cleaned data saved to {file_path}")

if __name__ == "__main__":
    clean_sentiment_scores()
