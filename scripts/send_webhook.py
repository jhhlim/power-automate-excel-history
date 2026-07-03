"""Send comparison results back to Power Automate via webhook."""

import os
import json
import requests
from pathlib import Path


def send_webhook():
    """
    Send the comparison results back to Power Automate webhook.
    """
    webhook_url = os.getenv('WEBHOOK_URL')
    
    if not webhook_url:
        print("No WEBHOOK_URL provided, skipping webhook notification")
        return True
    
    # Load the report
    report_path = Path('reports/report.json')
    
    if not report_path.exists():
        print(f"Error: Report file not found at {report_path}")
        return False
    
    try:
        with open(report_path, 'r') as f:
            report_data = json.load(f)
        
        print(f"Sending webhook to: {webhook_url}")
        
        # Send POST request to Power Automate
        response = requests.post(
            webhook_url,
            json=report_data,
            timeout=30,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code in [200, 201, 202]:
            print(f"Webhook sent successfully (Status: {response.status_code})")
            return True
        else:
            print(f"Webhook failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
    
    except requests.exceptions.RequestException as e:
        print(f"Error sending webhook: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


if __name__ == '__main__':
    success = send_webhook()
    exit(0 if success else 1)
