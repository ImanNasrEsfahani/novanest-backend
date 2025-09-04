"""Small test script to send a message through Mailgun HTTP API.

Usage:
  - Set MAILGUN_API_KEY, MAILGUN_DOMAIN, MAILGUN_FROM_EMAIL and TEST_EMAIL_TO (or MAILGUN_ADMIN_RECIPIENTS)
  - Run locally: python test_smtp.py
  - Or run inside the Docker web container so it uses the same network env: docker-compose exec web python test_smtp.py

This script prints HTTP status and response body for diagnostics.
"""
import os
import sys
from typing import List

try:
    import requests
except Exception as exc:
    print("The 'requests' package is required. Install it with: pip install requests", file=sys.stderr)
    raise


def _get_env(name: str, required: bool = False) -> str:
    val = os.getenv(name, "")
    if required and not val:
        print(f"Environment variable {name} is required but not set.", file=sys.stderr)
        sys.exit(2)
    return val


def _normalize_recipients(raw: str) -> List[str]:
    if not raw:
        return []
    # split on commas and semicolons
    parts = [p.strip() for p in raw.replace(';', ',').split(',') if p.strip()]
    return parts


def main():
    api_key = _get_env('MAILGUN_API_KEY', required=True)
    domain = _get_env('MAILGUN_DOMAIN', required=True)
    from_email = _get_env('MAILGUN_FROM_EMAIL', required=True)

    # Recipient: prefer TEST_EMAIL_TO, fallback to MAILGUN_ADMIN_RECIPIENTS
    to_raw = os.getenv('TEST_EMAIL_TO') or os.getenv('MAILGUN_ADMIN_RECIPIENTS')
    recipients = _normalize_recipients(to_raw)
    if not recipients:
        print('No recipients configured. Set TEST_EMAIL_TO or MAILGUN_ADMIN_RECIPIENTS.', file=sys.stderr)
        sys.exit(3)

    subject = os.getenv('TEST_EMAIL_SUBJECT', 'Mailgun test message from test_smtp.py')
    text = os.getenv('TEST_EMAIL_BODY', 'This is a test message sent by test_smtp.py')

    url = f'https://api.mailgun.net/v3/{domain}/messages'
    data = {
        'from': from_email,
        'to': recipients,
        'subject': subject,
        'text': text,
    }

    print('Sending Mailgun test message')
    print('  Domain:', domain)
    print('  From:', from_email)
    print('  To:', recipients)
    try:
        resp = requests.post(url, auth=('api', api_key), data=data, timeout=15)
    except requests.RequestException as exc:
        print('Request failed:', exc, file=sys.stderr)
        sys.exit(4)

    print('Response status:', resp.status_code)
    try:
        print('Response body:', resp.json())
    except Exception:
        print('Response body (text):', resp.text)

    if resp.ok:
        print('Mailgun test message sent successfully')
        return 0
    else:
        print('Mailgun returned an error status', file=sys.stderr)
        return 5


if __name__ == '__main__':
    sys.exit(main())
