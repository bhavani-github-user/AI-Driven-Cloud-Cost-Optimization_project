# Filename: CostAnomalyDetector.py
# Author: Bhavani
# Description: AWS Lambda function to detect cost anomalies using Cost Explorer,AI(Linear Regression)
# Created: 2025-05-22
# Updated: 2025-05-22

import json
import boto3
from datetime import date, timedelta
import os
threshold = float(event.get("threshold", os.environ.get("THRESHOLD", 0.10)))
email = event.get("email", os.environ.get("EMAIL", ""))


# How many past days to use for regression
REGRESSION_DAYS = 14

def lambda_handler(event, context):
    threshold = event.get("threshold", 0.10)
    email = event.get("email", "priyain3114141@gmail.com")
            
    if not email:
        return {"error": "Email is required in the event."
            }

    # Compute date window
    today = date.today()
    end_date = today - timedelta(days=1)              
    # up to yesterday
    start_date = end_date - timedelta(days=REGRESSION_DAYS - 1)

    start_str = start_date.strftime('%Y-%m-%d')
    end_str   = end_date.strftime('%Y-%m-%d')

    ce = boto3.client('ce', region_name='us-east-1')
    try:
      # 1) Fetch last REGRESSION_DAYS daily costs
      resp = ce.get_cost_and_usage(
         TimePeriod={'Start': start_str, 'End': end_str},
         Granularity='DAILY',
         Metrics=['UnblendedCost']

                                      )
      results = resp['ResultsByTime']
      # extract as list of floats in chronological order
      cost_data = [float(day['Total']['UnblendedCost']['Amount']) for day in results]

      # 2) Compute yesterday’s cost and compare to threshold
      yesterday_cost = cost_data[-1]
      if yesterday_cost < threshold:
        return {
          "message": (
          f"Yesterday's cost (${yesterday_cost:.2f}) did not exceed "
          f"threshold (${threshold:.2f}). No email sent."
                                                        )

                                                    }
      # 3) Linear regression on cost_data
      X = list(range(len(cost_data)))
      Y = cost_data
      n = len(X)
      sum_x  = sum(X)
      sum_y  = sum(Y)
      sum_xx = sum(x*x for x in X)
      sum_xy = sum(x*y for x, y in zip(X, Y))

      # slope (m) and intercept (b)
      m = (n*sum_xy - sum_x*sum_y) / (n*sum_xx - sum_x**2)
      b = (sum_y - m*sum_x) / n

      # 4) Predict next 7 days
      predictions = []
      start_idx = n
      for i in range(7):
        x = start_idx + i
        y = m * x + b
        predictions.append(round(y, 2))
            
      # Map dates to predictions
      pred_dates = [
        (today + timedelta(days=i)).strftime('%Y-%m-%d')
        for i in range(1, 8)
                                                                 ]
      forecast = dict(zip(pred_dates, predictions))
            
      # 5) Build email message
      lines = [
         "AWS Cost Alert & 7-Day Forecast\n",
         f"Date Checked : {end_str}",
         f"Cost         : ${yesterday_cost:.2f} (Threshold ${threshold:.2f})",
         "",
         "Next 7-Day Cost Forecast (Linear Regression):"
                                                                        ]
        for d, c in forecast.items():
            lines.append(f"  {d} : ${c:.2f}")
        body = "\n".join(lines)
            
       # 6) Send email via SES
       ses = boto3.client('ses', region_name='us-east-1')
       ses.send_email(
            Source=email,
            Destination={'ToAddresses': [email]},
            Message={
                'Subject': {'Data': 'AWS Daily Cost Alert & 7-Day Forecast'},
                'Body':    {'Text': {'Data': body}}
                

            }
            }
       return {
            "message": "Alert & forecast email sent successfully.",
            "checked_date": end_str,
            "checked_cost": yesterday_cost,
            "forecast": forecast
                                                                       }

    except Exception as e:
        return {"error": str(e)}

