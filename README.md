# Service Status Monitor

## Description

`Service-Status-Monitor` is a Python script that monitors the status of all system services on a Unix-like system. If any service is found to be down, the script sends notifications via Microsoft Teams and PagerDuty.

## Features

- Automatically detects and monitors all system services.
- Sends alerts to Microsoft Teams when a service is down.
- Creates PagerDuty incidents for any service failures.
- Logs activities and errors for troubleshooting.

## Requirements

- Python 3.x
- `requests` library
- `python-dotenv` library

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/realwib/Service-Status-Monitor.git
    cd Service-Status-Monitor
    ```

2. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Configure Environment Variables:**

    Configure the `.env` file in the root directory and add your credentials:

    ```dotenv
    PAGERDUTY_INTEGRATION_KEY=your_pagerduty_integration_key_here
    WEBHOOK_URL=your_teams_webhook_url_here
    ```

## Usage

Run the script as follows:

```bash
python service_status_checker.py
```
The script will check the status of all active system services and send notifications if any are down.

Logging
The script logs its activities to service_status_checker.log. Check this file for detailed information about the script's operations and any issues encountered.

