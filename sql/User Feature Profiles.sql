CREATE TABLE `saas-customer-base.churn_master_data.customer_feature_profiles` AS

WITH monthly_usage AS (
    -- Calculating Behavioral Decay (Month-over-Month change)
    SELECT 
        customer_id,
        log_month,
        login_count,
        LAG(login_count) OVER (PARTITION BY customer_id ORDER BY log_month) as prev_logins
    FROM `saas-customer-base.churn_master_data.fact_usage_logs`
),
usage_momentum AS (
    -- Getting only the most recent month's momentum
    SELECT 
        customer_id,
        ROUND(SAFE_DIVIDE((login_count - prev_logins), prev_logins) * 100, 1) as login_momentum
    FROM monthly_usage
    QUALIFY ROW_NUMBER() OVER(PARTITION BY customer_id ORDER BY log_month DESC) = 1
),
base_metrics AS (
    -- Preparing the core numbers for the logic
    SELECT 
        c.customer_id,
        c.company_name,
        c.segment,
        c.mrr,
        s.status as subscription_status,
        -- Convert Sentiment (-1 to 1) to Churn Prob (0 to 100)
        -- Formula: ((-Sentiment + 1) / 2) * 100
        ROUND(((-sent.sentiment_score + 1) / 2) * 100, 1) as churn_probability,
        -- MRR Classification
        CASE 
            WHEN c.mrr >= 5000 THEN 'High MRR'
            WHEN c.mrr >= 1500 THEN 'Medium MRR'
            ELSE 'Low MRR'
        END AS mrr_class,
        ROUND(u.avg_engagement, 1) as engagement
    FROM `saas-customer-base.churn_master_data.dim_customers` c
    LEFT JOIN `saas-customer-base.churn_master_data.fact_subscriptions` s ON c.customer_id = s.customer_id
    LEFT JOIN (SELECT customer_id, AVG(feature_engagement_score) as avg_engagement FROM `saas-customer-base.churn_master_data.fact_usage_logs` GROUP BY 1) u ON c.customer_id = u.customer_id
    LEFT JOIN (SELECT customer_id, AVG(sentiment_score) as sentiment_score FROM `saas-customer-base.churn_master_data.fact_support_tickets_scored` GROUP BY 1) sent ON c.customer_id = sent.customer_id
)

SELECT 
    b.*,
    m.login_momentum,
    -- Health Score: Weighted Engagement and Probability (Inverted)
    ROUND((b.engagement * 0.7) + ((100 - b.churn_probability) / 10 * 0.3), 1) as health_score,
    -- Your Custom Risk Category Logic
    CASE 
        WHEN b.subscription_status = 'Churned' THEN NULL
        WHEN b.churn_probability >= 75 AND b.mrr_class IN ('High MRR', 'Medium MRR') THEN 'High Risk'
        WHEN b.churn_probability >= 75 AND b.mrr_class = 'Low MRR' THEN 'Medium Risk'
        WHEN b.churn_probability >= 50 AND b.mrr_class IN ('High MRR', 'Medium MRR') THEN 'Medium Risk'
        WHEN b.churn_probability >= 50 AND b.mrr_class = 'Low MRR' THEN 'Low Risk'
        ELSE 'Low Risk'
    END AS risk_category
FROM base_metrics b
LEFT JOIN usage_momentum m ON b.customer_id = m.customer_id;