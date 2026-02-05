-- This creates a NEW permanent table from the 4 separate ones
CREATE OR REPLACE TABLE `saas-customer-base.churn_master_data.master_customer_table` AS

WITH usage_summary AS (
    -- Grouping usage logs to get averages per customer
    SELECT 
        customer_id,
        AVG(login_count) as avg_logins,
        AVG(feature_engagement_score) as avg_engagement
    FROM `saas-customer-base.churn_master_data.fact_usage_logs`
    GROUP BY 1
),
sentiment_summary AS (
    -- Bringing in your Python-cleaned sentiment data
    SELECT 
        customer_id,
        AVG(sentiment_score) as avg_sentiment_score,
        COUNT(ticket_id) as ticket_volume
    FROM `saas-customer-base.churn_master_data.sentiment_scored`
    GROUP BY 1
)

SELECT 
    c.customer_id,
    c.company_name,
    c.segment,
    c.mrr,
    s.status as subscription_status,
    u.avg_logins,
    u.avg_engagement,
    sent.avg_sentiment_score,
    sent.ticket_volume,
    -- Simple Logic: High Risk if sentiment is negative AND logins are low
    CASE 
        WHEN sent.avg_sentiment_score < 0 AND u.avg_logins < 5 THEN 'High Risk'
        WHEN sent.avg_sentiment_score < 0 OR u.avg_logins < 5 THEN 'Medium Risk'
        ELSE 'Low Risk'
    END AS risk_category
FROM `saas-customer-base.churn_master_data.dim_customers` c
LEFT JOIN `saas-customer-base.churn_master_data.fact_subscriptions` s ON c.customer_id = s.customer_id
LEFT JOIN usage_summary u ON c.customer_id = u.customer_id
LEFT JOIN sentiment_summary sent ON c.customer_id = sent.customer_id;