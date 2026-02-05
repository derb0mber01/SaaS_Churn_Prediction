import pandas as pd
import requests
from google.cloud import bigquery

# CONFIGURATION
N8N_WEBHOOK_URL = r"http://localhost:5678/webhook-test/retention-risk"
PROJECT_ID = "saas-customer-base"
SERVICE_ACCOUNT_FILE = r"C:\Users\uduok\git_folder\SaaS_Churn_Prediction\config\saas-customer-base-ddf412b72626.json"

# FETCH DATA
def get_risk_data():
    client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)
    
    query = """
    SELECT company_name, mrr, churn_probability, login_momentum
    FROM `churn_master_data.customer_feature_profiles`
    WHERE churn_probability > 60
    """
    return client.query(query).to_dataframe()

# RETENTION WARNING
def run_retention_guard():
    print("Connecting to BigQuery with Service Account...")
    df = get_risk_data()
    
    for _, row in df.iterrows():
        health_score = 100 - row['churn_probability']
        
        # Logic Gate: Automation only triggers for high-value targets
        if health_score < 40 and row['mrr'] > 500:
            payload = {
                "company": row['company_name'],
                "mrr": row['mrr'],
                "score": int(health_score),
                "momentum": row['login_momentum']
            }
            
            try:
                requests.post(N8N_WEBHOOK_URL, json=payload)
                print(f"✅ Alert sent for {row['company_name']}")
            except Exception as e:
                print(f"❌ Failed to reach n8n: {e}")

if __name__ == "__main__":
    run_retention_guard()