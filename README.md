
# AI-Driven-Cloud-Cost-optimization_project
# AWS Cost Monitoring and Prediction


## Project Summary

This project helps monitor and optimize AWS cloud costs by using two Lambda functions to detect anomalies and predict upcoming costs. It sends automated alerts via email and uses Terraform to manage Auto Scaling of EC2 instances, helping reduce unnecessary costs and improve efficiency.

---

## Key Features

- **EC2 Auto Scaling** using Terraform
- **Cost Anomaly Detection** using AWS Lambda
- **Cost Prediction for 7 Days** using AWS Cost Explorer
- **Automated Email Alerts** via AWS SES
- **IAM Roles & Policies** for secure Lambda access

---

## Technologies Used

- **Terraform**
- **AWS Lambda**
- **AWS Cost Explorer**
- **AWS Cost Anomaly Detection**
- **AWS SES**
- **IAM Roles & Policies**
- **Python (Boto3, Pandas)**
- **Ubuntu**

---

## Project Structure
---

## How It Works

1. **Terraform** sets up EC2 Auto Scaling groups to manage resources automatically.
2. **`aws-cost-alerts.py`**:
   - Runs daily using EventBridge
   - Predicts costs for the next 7 days via Cost Explorer
   - Sends email alerts using SES
3. **`CostAnomalyDetector.py`**:
   - Triggers when AWS detects a cost anomaly
   - Sends alert emails immediately
4. **IAM roles** provide access to Cost Explorer and SES.

---

## Setup Guide

### Prerequisites

- AWS Account (Free Tier)
- AWS CLI configured
- Python 3.x with `boto3` and `pandas`
- Terraform installed
- Verified email in AWS SES


