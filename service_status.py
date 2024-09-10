#!/usr/bin/env python3

import subprocess
import requests
import logging
import os

# Configuration from environment variables
PAGERDUTY_INTEGRATION_KEY = os.getenv("PAGERDUTY_INTEGRATION_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Ensure configuration is set
if not PAGERDUTY_INTEGRATION_KEY or not WEBHOOK_URL:
    raise ValueError("Environment variables PAGERDUTY_INTEGRATION_KEY and WEBHOOK_URL must be set.")

# Set up logging
logging.basicConfig(filename='service_status_checker.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_all_services():
    try:
        result = subprocess.run(['systemctl', 'list-units', '--type=service', '--state=active'], capture_output=True, text=True)
        services = [line.split()[0] for line in result.stdout.splitlines() if line.startswith(' ') and '.service' in line]
        return services
    except Exception as e:
        logging.error(f"Error getting list of services: {e}")
        return []

def get_service_status(service_name):
    try:
        result = subprocess.run(['systemctl', 'is-active', service_name], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        logging.error(f"Error checking service status: {e}")
        return None

def send_notification(service_name):
    # Send notification to Microsoft Teams
    message = f"Service {service_name} is down."
    payload = {"text": message}
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Error sending Microsoft Teams notification: {e}")

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
        logging.error(f"Error sending PagerDuty notification: {e}")

def main():
    services = get_all_services()
    for service in services:
        status = get_service_status(service)
        if status != "active":
            logging.info(f"Service {service} is down.")
            send_notification(service)

if __name__ == "__main__":
    main()
