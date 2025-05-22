import boto3
import json
from datetime import datetime, timedelta

# AWS Clients
ce_client = boto3.client('ce')
sns_client = boto3.client('sns')

def lambda_handler(event, context):
        today = datetime.today()
        
        # ----------- DAILY COST (Last 7 Days) -----------
        daily_end = (today - timedelta(days=1)).strftime('%Y-%m-%d')
        daily_start = (today - timedelta(days=8)).strftime('%Y-%m-%d')

        daily_response = ce_client.get_cost_and_usage(
            TimePeriod={'Start': daily_start, 'End': daily_end},
            Granularity='DAILY',
            Metrics=['UnblendedCost']
        )

        daily_total = 0.0
        daily_breakdown = "Daily Cost Breakdown (Last 7 Days):\n"
        for day in daily_response['ResultsByTime']:
                amount = float(day['Total']['UnblendedCost']['Amount'])
                date = day['TimePeriod']['Start']
                daily_breakdown += f"- {date}: ${amount:.2f}\n"
                daily_total += amount
            
            # ----------- MONTHLY COST (1st to Yesterday) -----------
        monthly_start = today.replace(day=1).strftime('%Y-%m-%d')
        monthly_end = (today - timedelta(days=1)).strftime('%Y-%m-%d')

        monthly_response = ce_client.get_cost_and_usage(
                TimePeriod={'Start': monthly_start, 'End': monthly_end},
                Granularity='MONTHLY',
                Metrics=['UnblendedCost']
                 
            )
        monthly_total = float(monthly_response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount'])

            # ----------- Thresholds -----------
        daily_threshold = 0.10
        monthly_threshold = 10.00
        alert_message = ""
        if daily_total > daily_threshold:
              alert_message += (
                f"**AWS Cost Alert: Daily Usage Exceeded**\n"
                f"Total (Last 7 Days): ${daily_total:.2f}\n"
                f"{daily_breakdown}\n"

            )
        if monthly_total > monthly_threshold:
                alert_message += (
                    f"**AWS Cost Alert: Monthly Usage Exceeded**\n"
                    f"Total (Month-to-Date): ${monthly_total:.2f}\n"
                    f"Billing Period: {monthly_start} to {monthly_end}\n"
                                                                            )

             # Print professional log output
        print("========== AWS COST MONITORING REPORT ==========")
        print(f"Daily Total (Last 7 Days): ${daily_total:.2f}")
        print(f"Monthly Total (Month-to-Date): ${monthly_total:.2f}")
        print("===============================================")

             # Send alert if any cost crosses threshold
        if alert_message:
                send_alert(alert_message)
        return {
                 "statusCode": 200,
                 "body": json.dumps({
                 "DailyTotal": round(daily_total, 2),
                "MonthlyTotal": round(monthly_total, 2)
                                                                        })
                                        }
# Function to send SNS alert
def send_alert(message):
        sns_client.publish(
                    TopicArn="arn:aws:sns:us-east-1:010526261255:CostAlertsTopic",
                    Message=message,
                    Subject="AWS Cost Alert: Threshold Breach Detected"
                                            )
