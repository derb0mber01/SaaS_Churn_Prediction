import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, timedelta

# Note: Ensure 'nltk' is installed in your environment (pip install nltk)
try:
    import nltk
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    nltk.download('vader_lexicon', quiet=True)
except ImportError:
    print("Warning: nltk not found. Run 'pip install nltk' to enable sentiment features later.")

# Set seed for reproducibility
np.random.seed(42)

# configuration
NUM_COMPANIES = 250
CHURN_RATE = 0.20 
TOTAL_CHURNERS = int(NUM_COMPANIES * CHURN_RATE)

# set the target directory
target_dir = r"C:\Users\uduok\git_folder\SaaS_Churn_Prediction\data\raw"

# generate dim_customers
customers = []
segments = ['Enterprise', 'Mid-Market', 'SMB']
for i in range(1, NUM_COMPANIES + 1):
    customers.append({
        'customer_id': i,
        'company_name': f"SaaS_Client_{i:03d}",
        'segment': random.choice(segments),
        'mrr': random.randint(500, 8000), 
        'setup_date': datetime(2025, 1, 1) + timedelta(days=random.randint(0, 45))
    })
df_customers = pd.DataFrame(customers)

# generate fact_subscriptions
churn_indices = random.sample(range(1, NUM_COMPANIES + 1), TOTAL_CHURNERS)
subscriptions = []
for i in range(1, NUM_COMPANIES + 1):
    is_churned = i in churn_indices
    status = 'Churned' if is_churned else 'Active'
    churn_date = datetime(2025, 6, 1) + timedelta(days=random.randint(1, 30)) if is_churned else None
    subscriptions.append({
        'customer_id': i,
        'status': status,
        'churn_date': churn_date
    })
df_subs = pd.DataFrame(subscriptions)

# generate fact_usage_logs
usage_data = []
for i in range(1, NUM_COMPANIES + 1):
    is_churner = i in churn_indices
    for month in range(1, 7): 
        decay_factor = (0.82 ** month) if is_churner else (1.02 ** month)
        base_logins = 120 * decay_factor
        
        usage_data.append({
            'customer_id': i,
            'log_month': month,
            'login_count': int(max(0, np.random.normal(base_logins, 8))),
            'feature_engagement_score': round(max(0, np.random.normal(70 * decay_factor, 5)), 2)
        })
df_usage = pd.DataFrame(usage_data)

# generate fact_support_tickets
tickets = []
complaints = [
    "Security audit failed due to your outdated SSO implementation.",
    "The Salesforce integration is dropping leads; this is costing us revenue.",
    "API documentation is inconsistent with the actual endpoints.",
    "UI is extremely sluggish when loading large datasets. Unusable for our team.",
    "Major regression found in the latest deployment—reporting is broken.",
    "Pricing has increased 20% but we haven't seen any new features in months.",
    "Our procurement department is questioning the ROI of this contract.",
    "Bulk export to CSV keeps timing out for our Enterprise account.",
    "The mobile app is crashing on startup after the iOS update.",
    "Too many clicks to reach the main dashboard. UX is frustrating."
]

praise = [
    "The new automated workflow saved our team 10 hours this week!",
    "Incredible response time from the technical support team.",
    "The dashboard is beautiful and very intuitive for our executives.",
    "Integration with Slack was seamless. Love the notifications.",
    "Best-in-class API documentation. We got up and running in a day.",
    "Really appreciate the proactive check-in from our Success Manager.",
    "The latest feature release is exactly what we were looking for.",
    "Higher ROI than the previous vendor we used. Great value.",
    "Super fast load times even with our massive database.",
    "The custom reporting tool is a game changer for our QBRs."
]

neutral_queries = [
    "How do I reset the password for a sub-user?",
    "Where can I find the invoice for March 2025?",
    "Can you provide the IP range for whitelisting?",
    "Does the current plan support multi-factor authentication?",
    "Is there a limit on the number of API calls per minute?",
    "Updating our billing address—who should I send this to?",
    "Requesting a copy of the latest SOC2 Type II report.",
    "Quick question about the upcoming webinar schedule."
]

for i in range(1, NUM_COMPANIES + 1):
    is_churner = i in churn_indices
    num_tickets = random.randint(3, 8) if is_churner else random.randint(1, 4)
    
    for _ in range(num_tickets):
        rand = random.random()
        if is_churner:
            text = np.random.choice(complaints) if rand < 0.7 else np.random.choice(neutral_queries + praise)
        else:
            text = np.random.choice(praise) if rand < 0.5 else np.random.choice(neutral_queries + complaints)
            
        tickets.append({
            'customer_id': i,
            'ticket_id': random.randint(100000, 999999),
            'ticket_category': 'Technical' if 'API' in text or 'integration' in text.lower() else 'Account',
            'ticket_text': text,
            'priority': 'High' if (is_churner and random.random() > 0.3) else 'Low',
            'created_at': datetime(2025, 1, 1) + timedelta(days=random.randint(0, 150))
        })
df_tickets = pd.DataFrame(tickets)

# export files

df_customers.to_csv(os.path.join(target_dir, 'dim_customers.csv'), index=False)
df_subs.to_csv(os.path.join(target_dir, 'fact_subscriptions.csv'), index=False)
df_usage.to_csv(os.path.join(target_dir, 'fact_usage_logs.csv'), index=False)
df_tickets.to_csv(os.path.join(target_dir, 'fact_support_tickets.csv'), index=False)

print("-" * 30)
print(f"SUCCESS: Dataset generated for {NUM_COMPANIES} companies.")
print(f"FILES SAVED TO: {target_dir}")
print(f"Total Usage Logs: {len(df_usage)}")
print(f"Total Support Tickets: {len(df_tickets)}")
print("-" * 30)
