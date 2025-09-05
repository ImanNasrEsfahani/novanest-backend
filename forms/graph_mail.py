import logging
import requests
import msal
from django.conf import settings
from django.template.loader import render_to_string
from typing import Sequence, Optional

logger = logging.getLogger(__name__)

_SCOPES = ["https://graph.microsoft.com/.default"]
_TOKEN_CACHE = None  # simple module-level cache


def _get_access_token() -> Optional[str]:
    if not settings.MS_GRAPH_USE:
        return None
    global _TOKEN_CACHE
    if _TOKEN_CACHE is None:
        _TOKEN_CACHE = msal.TokenCache()
    app = msal.ConfidentialClientApplication(
        client_id=settings.MS_GRAPH_CLIENT_ID,
        client_credential=settings.MS_GRAPH_CLIENT_SECRET,
        authority=f"https://login.microsoftonline.com/{settings.MS_GRAPH_TENANT_ID}",
        token_cache=_TOKEN_CACHE,
    )
    # Try cache first
    result = app.acquire_token_silent(_SCOPES, account=None)
    if not result:
        result = app.acquire_token_for_client(scopes=_SCOPES)
    if 'access_token' not in result:
        logger.error("MS Graph token acquisition failed: %s", result.get('error_description'))
        return None
    return result['access_token']


def send_graph_mail(subject: str, html_template: str, context: dict, to_emails: Sequence[str], text_fallback: Optional[str] = None) -> bool:
    """Send an email via Microsoft Graph. Returns True on success."""
    if not settings.MS_GRAPH_USE:
        logger.debug("MS Graph not configured; skipping Graph send.")
        return False
    access_token = _get_access_token()
    if not access_token:
        return False
    html_body = render_to_string(html_template, context)
    if not text_fallback:
        # crude text fallback strip tags
        text_fallback = ''.join(html_body.split('<'))  # minimal; improve if needed
    payload = {
        "message": {
            "subject": subject,
            "body": {"contentType": "HTML", "content": html_body},
            "from": {"emailAddress": {"address": settings.MS_GRAPH_SENDER}},
            "sender": {"emailAddress": {"address": settings.MS_GRAPH_SENDER}},
            "toRecipients": [
                {"emailAddress": {"address": addr}} for addr in to_emails
            ],
        },
        "saveToSentItems": True,
    }
    resp = requests.post(
        "https://graph.microsoft.com/v1.0/users/{}/sendMail".format(settings.MS_GRAPH_SENDER),
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )
    if resp.status_code in (202, 200):
        return True
    logger.error("Graph send failed %s: %s", resp.status_code, resp.text)
    return False
