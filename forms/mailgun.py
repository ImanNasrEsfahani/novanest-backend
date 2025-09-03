import logging
from typing import Iterable, Optional, Union

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def _get_mailgun_config():
    """Return (domain, api_key, from_email) from settings or env defaults."""
    domain = getattr(settings, "MAILGUN_DOMAIN", None)
    api_key = getattr(settings, "MAILGUN_API_KEY", None)
    from_email = getattr(settings, "MAILGUN_FROM_EMAIL", None)
    return domain, api_key, from_email


def send_mailgun_message(
    to: Union[str, Iterable[str]],
    subject: str,
    text: str,
    html: Optional[str] = None,
    from_email: Optional[str] = None,
    cc: Optional[Union[str, Iterable[str]]] = None,
    bcc: Optional[Union[str, Iterable[str]]] = None,
    timeout: int = 10,
) -> Optional[requests.Response]:
    """
    Send an email using the Mailgun HTTP API.

    Returns the requests.Response on success (status_code 200/201) or None on failure.

    Parameters:
    - to: recipient email or iterable of emails
    - subject: email subject
    - text: plain-text body
    - html: optional HTML body
    - from_email: optional override for the From address
    - cc, bcc: optional CC/BCC recipients
    - timeout: request timeout in seconds
    """
    domain, api_key, default_from = _get_mailgun_config()
    if not domain or not api_key:
        logger.error("Mailgun not configured: MAILGUN_DOMAIN or MAILGUN_API_KEY missing")
        return None

    from_email = from_email or default_from
    if not from_email:
        logger.error("Mailgun from address not configured (MAILGUN_FROM_EMAIL)")
        return None

    # Normalize recipients to lists
    def _norm(x):
        if x is None:
            return None
        if isinstance(x, (list, tuple)):
            return list(x)
        return [x]

    to_list = _norm(to)
    cc_list = _norm(cc)
    bcc_list = _norm(bcc)

    data = {
        "from": from_email,
        "to": to_list,
        "subject": subject,
        "text": text,
    }
    if html:
        data["html"] = html
    if cc_list:
        data["cc"] = cc_list
    if bcc_list:
        data["bcc"] = bcc_list

    url = f"https://api.mailgun.net/v3/{domain}/messages"
    try:
        resp = requests.post(url, auth=("api", api_key), data=data, timeout=timeout)
        resp.raise_for_status()
        logger.info("Mailgun message sent to %s (subject=%s) status=%s", to_list, subject, resp.status_code)
        return resp
    except requests.RequestException as exc:
        # Log the error and return None for the caller to handle
        logger.exception("Mailgun send failed: %s", exc)
        return None


def send_simple_message():
    """Compatibility helper similar to the snippet provided; sends to the configured admin recipient(s)."""
    domain, api_key, from_email = _get_mailgun_config()
    if not domain or not api_key or not from_email:
        logger.error("Mailgun configuration incomplete for send_simple_message")
        return None

    admin_recipients = getattr(settings, "MAILGUN_ADMIN_RECIPIENTS", None)
    if not admin_recipients:
        logger.error("MAILGUN_ADMIN_RECIPIENTS not set; cannot send_simple_message")
        return None

    return send_mailgun_message(
        to=admin_recipients,
        subject="Hello NovaNestVenture",
        text="Congratulations NovaNestVenture, you just sent an email with Mailgun! You are truly awesome!",
        from_email=from_email,
    )


__all__ = ["send_mailgun_message", "send_simple_message"]
