# Service Status Monitor

This repository contains a Python script to monitor the status of specified system services. The script checks if the services are running and sends notifications to Microsoft Teams and PagerDuty if any service is down.

## Features

- Monitors the status of multiple system services.
- Sends notifications to Microsoft Teams and PagerDuty when a service is down.
- Customizable list of services to monitor.

## Prerequisites

Ensure you have Python 3 and the necessary libraries installed:

- `requests`

You can install the required libraries using pip:

```bash
pip install requests
```

## Configuration

1. **PagerDuty Integration Key:** Update the `PAGERDUTY_INTEGRATION_KEY` variable in the `service_status_checker.py` file with your PagerDuty integration key.

2. **Microsoft Teams Webhook URL:** Update the `WEBHOOK_URL` variable in the `service_status_checker.py` file with your Microsoft Teams webhook URL.

3. **Services List:** Modify the `services` list in the `main()` function of `service_status_checker.py` to include the services you want to monitor.

## Usage

1. **Clone the repository:**

    ```bash
    git clone https://github.com/realwib/Service-Status-Monitor.git
    cd Service-Status-Monitor
    ```

2. **Install dependencies:**

    ```bash
    pip install requests
    ```

3. **Run the script:**

    ```bash
    python service_status.py
    ```

    The script will check the status of the specified services and send notifications if any service is found to be down.
