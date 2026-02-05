# SaaS\Churn\Prediction \& Revenue Recovery


<img width="1203" height="705" alt="image" src="https://github.com/user-attachments/assets/f7621311-a92f-48cd-8818-42af5b255b92" />

Churn &amp; Revenue Analysis for Customer Retention in a Fast Growing SaaS Startup


Problem Statement:
A B2B SaaS startup is growing rapidly but quietly losing customers. Revenue looks healthy, but the "Silent Churn" decaying product usage and unresolved technical frustration threatens the upcoming Series B funding round. This project builds an early-warning system to identify at-risk accounts before they cancel.





Technical Architecture:
This repository contains a production-grade data pipeline:

* Data Generation: Python engine simulating 250+ companies with realistic behavioral decay (15-20% monthly usage drops).
* NLP Pipeline: Sentiment analysis and keyword extraction from unstructured support tickets using Python.
* Cloud Warehouse: Google BigQuery serves as the source of truth, joining behavioral logs with sentiment scores via SQL.
* Automation Layer: An n8n orchestration engine (self-hosted via Docker) that monitors the warehouse.
* GTM Activation: A Python-based "Retention Guard" that triggers real-time Slack alerts for high-value/high-risk accounts.





Repository Structure:

* scripts: Data cleaning, BigQuery ingestion, and the "Retention Guard" trigger logic.
* sql: Analytical queries and table schemas used in the BigQuery warehouse.
* data: Tiered storage containing `/raw` inputs, `/processed` sentiment data, and `/results` (exported BigQuery risk scores).
* notebooks: Exploratory Data Analysis (EDA) and churn probability modeling.
* reports: Interactive Power BI dashboard for executive-level retention monitoring.





Problems Solved:

* Quantifies Qualitative Risk: Translates messy support ticket text into a numerical "Sentiment Score".
* Predictive Behavioral Tracking: Detects "Login Momentum" decay months before it manifests as a cancellation request.
* Automated Intervention: Moves Customer Support teams from reactive dashboards to proactive Slack alerts, ensuring zero-latency outreach.
* Revenue Protection: Prioritizes retention efforts by filtering alerts based on Account MRR thresholds.
