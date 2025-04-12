from db.models import Email
from .rule_schema import RuleSet, Rule, RuleCondition, RuleAction
from sqlalchemy.orm import Session
from typing import List, Tuple
import json
import os
from datetime import datetime, timedelta


def load_rules(path: str = "rules/rules.json") -> RuleSet:
    with open(path, "r") as f:
        data = json.load(f)
    return RuleSet(**data)


def match_condition(email: Email, cond: RuleCondition) -> bool:
    val = cond.value
    field = cond.field

    # Map model fields
    attr = {
        "from": email.sender,
        "subject": email.subject,
        "message": email.message_snippet,
        "received_at": email.received_at
    }.get(field)

    if field == "received_at":
        if cond.predicate == "less_than_days":
            return (datetime.utcnow() - attr) < timedelta(days=int(val))
        elif cond.predicate == "greater_than_days":
            return (datetime.utcnow() - attr) > timedelta(days=int(val))
        elif cond.predicate == "less_than_months":
            return (datetime.utcnow() - attr) < timedelta(days=30 * int(val))
        elif cond.predicate == "greater_than_months":
            return (datetime.utcnow() - attr) > timedelta(days=30 * int(val))
    else:
        attr = attr.lower() if attr else ""
        val = val.lower()

        if cond.predicate == "contains":
            return val in attr
        elif cond.predicate == "does_not_contain":
            return val not in attr
        elif cond.predicate == "equals":
            return attr == val
        elif cond.predicate == "does_not_equal":
            return attr != val

    return False


def apply_rules(db: Session, ruleset: RuleSet) -> List[Tuple[Email, List[RuleAction]]]:
    applicable = []

    all_emails = db.query(Email).all()
    for email in all_emails:
        for rule in ruleset.rules:
            matches = [match_condition(email, cond) for cond in rule.rules]

            if (rule.predicate == "all" and all(matches)) or (rule.predicate == "any" and any(matches)):
                applicable.append((email, rule.actions))
                break  # skip other rules for this email

    return applicable