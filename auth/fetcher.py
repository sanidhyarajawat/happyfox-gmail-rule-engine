from googleapiclient.discovery import Resource
from email.utils import parsedate_to_datetime
from sqlalchemy.orm import Session
from db.models import Email
from datetime import datetime
import base64
import logging

logger = logging.getLogger(__name__)


def fetch_and_store_emails(service: Resource, db: Session, max_results: int = 20):
    """Fetch latest emails from Gmail and store in DB if not already present."""
    results = service.users().messages().list(userId='me', maxResults=max_results, q="in:inbox").execute()
    messages = results.get('messages', [])

    logger.info(f"Fetched {len(messages)} messages.")

    for msg in messages:
        msg_id = msg['id']

        # Skip if already in DB
        if db.query(Email).filter_by(gmail_id=msg_id).first():
            continue

        # Fetch full message
        message = service.users().messages().get(userId='me', id=msg_id, format='full').execute()

        headers = {h['name'].lower(): h['value'] for h in message['payload'].get('headers', [])}

        sender = headers.get('from', '')
        recipient = headers.get('to', '')
        subject = headers.get('subject', '')
        date_str = headers.get('date', '')

        received_at = None
        try:
            received_at = parsedate_to_datetime(date_str)
        except Exception:
            logger.warning(f"Could not parse date: {date_str}")

        snippet = message.get('snippet', '')

        label_ids = message.get('labelIds', [])
        is_read = 'UNREAD' not in label_ids

        email = Email(
            gmail_id=msg_id,
            sender=sender,
            recipient=recipient,
            subject=subject,
            message_snippet=snippet,
            received_at=received_at or datetime.utcnow(),
            labels=label_ids,
            is_read=is_read
        )

        db.add(email)
        logger.info(f"Storing email from {sender} with subject '{subject}'")

    db.commit()