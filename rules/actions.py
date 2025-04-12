from googleapiclient.discovery import Resource
from db.models import Email
from .rule_schema import RuleAction
from typing import List
import logging

logger = logging.getLogger(__name__)


def mark_as_read(service: Resource, gmail_id: str):
    service.users().messages().modify(
        userId='me',
        id=gmail_id,
        body={"removeLabelIds": ["UNREAD"]}
    ).execute()
    logger.info(f"Marked {gmail_id} as read")


def mark_as_unread(service: Resource, gmail_id: str):
    service.users().messages().modify(
        userId='me',
        id=gmail_id,
        body={"addLabelIds": ["UNREAD"]}
    ).execute()
    logger.info(f"Marked {gmail_id} as unread")


def apply_label(service: Resource, gmail_id: str, label_name: str):
    """Add label to a message. Create label if it doesn't exist."""
    # Get all labels
    existing_labels = service.users().labels().list(userId='me').execute().get("labels", [])
    label_id = None

    for label in existing_labels:
        if label["name"].lower() == label_name.lower():
            label_id = label["id"]
            break

    # If label doesn't exist, create it
    if not label_id:
        new_label = service.users().labels().create(userId='me', body={
            "name": label_name,
            "labelListVisibility": "labelShow",
            "messageListVisibility": "show"
        }).execute()
        label_id = new_label["id"]

    # Apply label and remove from INBOX
    service.users().messages().modify(
        userId='me',
        id=gmail_id,
        body={
            "addLabelIds": [label_id],
            "removeLabelIds": ["INBOX"]
        }
    ).execute()
    logger.info(f"Moved {gmail_id} to label '{label_name}'")


def execute_actions(service: Resource, email: Email, actions: List[RuleAction]):
    for action in actions:
        if action.type == "mark_as_read":
            mark_as_read(service, email.gmail_id)
        elif action.type == "mark_as_unread":
            mark_as_unread(service, email.gmail_id)
        elif action.type == "move" and action.label:
            apply_label(service, email.gmail_id, action.label)