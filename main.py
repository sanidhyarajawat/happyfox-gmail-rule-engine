from auth.gmail_auth import get_gmail_service
from db.database import SessionLocal, init_db
from auth.fetcher import fetch_and_store_emails
from rules.rules_engine import load_rules, apply_rules
from rules.actions import execute_actions

import logging

logging.basicConfig(level=logging.INFO)

def main():
    # Step 1: Init DB and Gmail API
    init_db()
    db = SessionLocal()
    service = get_gmail_service()

    # Step 2: Fetch and store emails
    fetch_and_store_emails(service, db)

    # Step 3: Load rules and apply them
    ruleset = load_rules()
    matches = apply_rules(db, ruleset)

    # Step 4: Execute actions for matching emails
    for email, actions in matches:
        execute_actions(service, email, actions)

    db.close()
    logging.info("Done processing rules.")

if __name__ == "__main__":
    main()
