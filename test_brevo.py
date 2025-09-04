"""Quick Brevo SMTP test script.

Usage:
  - Set BREVO_SMTP_LOGIN, BREVO_SMTP_PASSWORD, BREVO_FROM_EMAIL, TEST_EMAIL_TO
  - Optional: BREVO_SMTP_HOST (default smtp-relay.brevo.com), BREVO_SMTP_PORT (default 587)
  - Run: python test_brevo.py

This script uses smtplib directly to avoid importing Django when running locally.
"""
import os
import sys
import smtplib
from email.message import EmailMessage


def _get_env(name: str, required: bool = False) -> str:
    val = os.getenv(name, "")
    if required and not val:
        print(f"Environment variable {name} is required but not set.", file=sys.stderr)
        sys.exit(2)
    return val


def main():
    host = os.getenv('BREVO_SMTP_HOST', 'smtp-relay.brevo.com')
    port = int(os.getenv('BREVO_SMTP_PORT', '587'))
    login = _get_env('BREVO_SMTP_LOGIN', required=True)
    password = _get_env('BREVO_SMTP_PASSWORD', required=True)
    from_email = _get_env('BREVO_FROM_EMAIL', required=True)
    to_raw = _get_env('TEST_EMAIL_TO', required=True)
    to_list = [p.strip() for p in to_raw.replace(';', ',').split(',') if p.strip()]

    subject = os.getenv('TEST_EMAIL_SUBJECT', 'Brevo SMTP test message')
    text = os.getenv('TEST_EMAIL_BODY', 'This is a test message sent by test_brevo.py')

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = ', '.join(to_list)
    msg.set_content(text)

    print('Sending Brevo SMTP test message')
    print('  Host:', host)
    print('  Port:', port)
    print('  From:', from_email)
    print('  To:', to_list)

    try:
        with smtplib.SMTP(host, port, timeout=15) as smtp:
            smtp.ehlo()
            if port == 587:
                smtp.starttls()
                smtp.ehlo()
            smtp.login(login, password)
            smtp.send_message(msg, from_addr=from_email, to_addrs=to_list)
    except Exception as exc:
        print('Failed to send Brevo SMTP test message:', exc, file=sys.stderr)
        return 1

    print('Brevo SMTP test message sent successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
