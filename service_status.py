#!/usr/bin/env python3

import subprocess
import requests
import sys

# Replace these with your actual credentials
PAGERDUTY_INTEGRATION_KEY = "<YOUR_PAGERDUTY_INTEGRATION_KEY>"
WEBHOOK_URL = "<YOUR_MICROSOFT_TEAMS_WEBHOOK_URL>"

def get_service_status(service_name):
    try:
        result = subprocess.run(['systemctl', 'is-active', service_name], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"Error checking service status: {e}", file=sys.stderr)
        return None

def send_notification(service_name):
    # Send notification to Microsoft Teams
    message = f"Service {service_name} is down."
    payload = {"text": message}
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error sending Microsoft Teams notification: {e}", file=sys.stderr)

    # Send incident to PagerDuty
    pagerduty_payload = {
        "routing_key": PAGERDUTY_INTEGRATION_KEY,
        "event_action": "trigger",
        "payload": {
            "summary": f"Service {service_name} is down.",
            "source": "service-status-checker",
            "severity": "critical",
            "component": service_name,
            "group": "service-status",
            "class": "service-status"
        }
    }

    try:
        pd_response = requests.post("https://events.pagerduty.com/v2/enqueue", json=pagerduty_payload)
        pd_response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error sending PagerDuty notification: {e}", file=sys.stderr)

def main():
    services = ["nginx", "apache2", "mysql"]  # Add your services here
    
    for service in services:
        status = get_service_status(service)
        if status != "active":
            print(f"Service {service} is down.")
            send_notification(service)

if __name__ == "__main__":
    main()
