import boto3
import json

# AWS Cost Explorer Client
client = boto3.client('ce')
sns_client = boto3.client('sns')

def lambda_handler(event, context):
            # Define the time period (last 7 days)
                from datetime import datetime, timedelta
                end_date = datetime.today().strftime('%Y-%m-%d')
                start_date = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')

                # Fetch cost data
                response = client.get_cost_and_usage(
                TimePeriod={'Start': start_date, 'End': end_date},
                Granularity='DAILY',
                Metrics=['BlendedCost']
                )

                # Extract cost values
                total_cost = sum(float(day['Total']['BlendedCost']['Amount']) for day in response['ResultsByTime'])

                # Set a cost threshold (e.g., $o.10)
                cost_threshold = 0.10

                if total_cost > cost_threshold:
                  alert_message = f"⚠️ ALERT: AWS cost exceeded! Total Cost: ${total_cost:.2f}"
                  print(alert_message)
                  send_alert(alert_message)

                  return {"statusCode": 200, "body": json.dumps({"TotalCost": total_cost})}

                # Function to send email alert (Optional)
                def send_alert(message):
                    sns_client = boto3.client('sns')
                    sns_client.publish(
                    TopicArn="arn:aws:sns:us-east-1:010526261255:CostAlertsTopic",
                    Message=message,                                                                                                                      Subject="AWS Cost Alert"                                                                                        )

